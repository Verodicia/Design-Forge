#!/usr/bin/env python3
"""
forge.py — Design Forge command-line tool (Python 3.8+, standard library only).

Usage (run from the repository root):
  python3 tools/forge.py spawn <dir> <slug> "<Game Name>"  (base only) create a new GAME repo
  python3 tools/forge.py upgrade                           (game repo) pull platform updates + sync
  python3 tools/forge.py sync [<slug>]                     add new template files/coverage rows to projects
  python3 tools/forge.py new <slug> "<Game Name>"         create a project (game repos; --force in base)
  python3 tools/forge.py list                              list projects
  python3 tools/forge.py board <slug>                      regenerate projects/<slug>/BOARD.md
  python3 tools/forge.py next <slug> --tier T2 [--caps web,code] [--role systems-designer] [--any-phase]
  python3 tools/forge.py claim <slug> <TASK-ID> --agent "<model>" --tier T2 --role <role> [--caps ...]
  python3 tools/forge.py id <slug> task|question|decision <CODE>
  python3 tools/forge.py create <slug> task|question|decision <CODE> "<title>" [options]
  python3 tools/forge.py decompose <slug> [--max-phase N] [--discipline 01-mechanics] [--dry-run]
  python3 tools/forge.py validate <slug>|--all
  python3 tools/forge.py guide <slug>                      compile guide/_compiled.md

See AGENTS.md for how agents use these commands.
"""
import argparse
import datetime as _dt
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS = os.path.join(ROOT, "projects")
TEMPLATE = os.path.join(PROJECTS, "_template")
PLATFORM = os.path.join(ROOT, "platform")

ROLES = {
    "ORC": "orchestrator", "REV": "reviewer", "CD": "creative-director",
    "SYS": "systems-designer", "NAR": "narrative-designer", "LVL": "level-designer",
    "ART": "art-director", "AUD": "audio-director", "UX": "ux-designer",
    "TECH": "technical-director", "ECO": "economy-designer", "BIZ": "business-strategist",
    "PROD": "producer", "QA": "qa-lead", "GUIDE": "guide-writer",
}
ROLE_CODES = {v: k for k, v in ROLES.items()}
TIERS = {"T1": 1, "T2": 2, "T3": 3}  # lower number = more capable
CAPS = {"web", "code", "image-gen", "image-read", "long-context", "human"}
TASK_STATUSES = {"open", "claimed", "waiting", "blocked", "review", "done", "cancelled"}
Q_STATUSES = {"open", "answered", "processed"}
D_STATUSES = {"proposed", "locked", "superseded"}
PAGE_STATUSES = {"stub", "exploring", "draft", "locked", "n/a", "superseded"}
PRIORITIES = {"blocking": 0, "high": 1, "normal": 2, "low": 3}
KINDS = {"task": ("T", "tasks"), "question": ("Q", "questions"), "decision": ("D", "decisions")}
HEDGES = [r"maybe", r"might", r"perhaps", r"possibly", r"probably", r"could be", r"tbd",
          r"todo", r"to be decided", r"we'll see", r"something like", r"roughly",
          r"ideally", r"hopefully", r"\?\?\?"]
HEDGE_RE = re.compile(r"(?<![\w-])(" + "|".join(HEDGES) + r")(?![\w-])", re.I)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
ID_RE = re.compile(r"^([TQD])-([A-Z]+)-(\d{4})$")


# ----------------------------------------------------------------- helpers
def today():
    return _dt.date.today().isoformat()


def now():
    return _dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ")


def die(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def split_fm(text):
    """Return (frontmatter_lines, body) or (None, text)."""
    if not text.startswith("---"):
        return None, text
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "\n".join(lines[i + 1:])
    return None, text


def parse_value(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    if v.lower() in ("true", "false"):
        return v.lower() == "true"
    return v


def parse_fm(text):
    lines, _ = split_fm(text)
    if lines is None:
        return None
    data = {}
    for line in lines:
        if not line or line[0] in " \t#":
            continue  # nested / comment lines are ignored by this simple parser
        if ":" in line:
            k, v = line.split(":", 1)
            v = re.sub(r"\s+#.*$", "", v)  # strip trailing comments
            data[k.strip()] = parse_value(v)
    return data


def fmt_value(v):
    if isinstance(v, list):
        return "[" + ", ".join(v) + "]"
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def set_fm(path, updates):
    text = read(path)
    lines, body = split_fm(text)
    if lines is None:
        die("no frontmatter in " + path)
    for k, v in updates.items():
        new = "%s: %s" % (k, fmt_value(v))
        for i, line in enumerate(lines):
            if re.match(r"^%s\s*:" % re.escape(k), line):
                lines[i] = new
                break
        else:
            lines.append(new)
    write(path, "---\n" + "\n".join(lines) + "\n---\n" + body)


def append_log(path, line):
    text = read(path).rstrip("\n") + "\n- " + line + "\n"
    write(path, text)


def project_dir(slug):
    p = os.path.join(PROJECTS, slug)
    if not os.path.isdir(p):
        die("no project '%s' (see: forge.py list)" % slug)
    return p


def md_files(folder):
    out = []
    for dp, _, fns in os.walk(folder):
        for fn in sorted(fns):
            if fn.endswith(".md"):
                out.append(os.path.join(dp, fn))
    return sorted(out)


def load_items(pdir, kind):
    """Return {id: (path, frontmatter)} for tasks / questions / decisions."""
    sub = KINDS[kind][1]
    items = {}
    for p in md_files(os.path.join(pdir, sub)):
        fm = parse_fm(read(p)) or {}
        if fm.get("id"):
            items[fm["id"]] = (p, fm)
    return items


def project_phase(pdir):
    fm = parse_fm(read(os.path.join(pdir, "PROJECT.md"))) or {}
    try:
        return int(fm.get("phase", 0))
    except ValueError:
        return 0


def disciplines(pdir):
    w = os.path.join(pdir, "wiki")
    return sorted(d for d in os.listdir(w) if os.path.isfile(os.path.join(w, d, "index.md")))


def coverage_rows(pdir):
    """Yield dicts for every coverage-map row in every discipline index."""
    rows = []
    for d in disciplines(pdir):
        path = os.path.join(pdir, "wiki", d, "index.md")
        fm = parse_fm(read(path)) or {}
        for n, line in enumerate(read(path).split("\n")):
            if not line.startswith("| `"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            while len(cells) < 8:
                cells.append("")
            rows.append({
                "discipline": d, "path": path, "line": n, "owner": fm.get("owner", ""),
                "key": cells[0].strip("`"), "topic": cells[1], "tier": cells[2] or "T2",
                "needs": [x.strip() for x in cells[3].split(",") if x.strip()],
                "phase": cells[4], "status": cells[5] or "stub", "page": cells[6], "ref": cells[7],
            })
    return rows


def set_row_cell(row, col, value):
    lines = read(row["path"]).split("\n")
    cells = [c.strip() for c in lines[row["line"]].strip().strip("|").split("|")]
    while len(cells) < 8:
        cells.append("")
    cells[col] = value
    lines[row["line"]] = "| " + " | ".join(cells) + " |"
    write(row["path"], "\n".join(lines))


def next_id(pdir, kind, code):
    code = code.upper()
    if code not in ROLES:
        die("unknown role code '%s'. Known: %s" % (code, ", ".join(ROLES)))
    prefix = KINDS[kind][0]
    n = 0
    for p in md_files(os.path.join(pdir, KINDS[kind][1])):
        m = ID_RE.match(os.path.splitext(os.path.basename(p))[0])
        if m and m.group(1) == prefix and m.group(2) == code:
            n = max(n, int(m.group(3)))
    return "%s-%s-%04d" % (prefix, code, n + 1)


def fill(template_text, **kw):
    for k, v in kw.items():
        template_text = template_text.replace("{{%s}}" % k, str(v))
    return template_text


def is_game_repo():
    """Game repos carry a .forge-game marker (written by `spawn`). The clean base never does."""
    return os.path.exists(os.path.join(ROOT, ".forge-game"))


def platform_version():
    p = os.path.join(PLATFORM, "VERSION")
    return read(p).strip() if os.path.exists(p) else "0.0.0"


def git(*args, cwd=None, check=True):
    r = subprocess.run(["git"] + list(args), cwd=cwd or ROOT, capture_output=True, text=True)
    if check and r.returncode != 0:
        die("git %s failed:\n%s" % (" ".join(args), (r.stderr or r.stdout).strip()))
    return r.stdout.strip()


def game_projects():
    return [os.path.join(PROJECTS, d) for d in sorted(os.listdir(PROJECTS))
            if not d.startswith("_") and os.path.isfile(os.path.join(PROJECTS, d, "PROJECT.md"))]


# ----------------------------------------------------------------- commands
def cmd_list(a):
    for d in sorted(os.listdir(PROJECTS)):
        p = os.path.join(PROJECTS, d)
        if d.startswith("_") or not os.path.isdir(p):
            continue
        fm = parse_fm(read(os.path.join(p, "PROJECT.md"))) or {}
        print("%-24s phase %s  %s" % (d, fm.get("phase", "?"), fm.get("name", "")))


def cmd_new(a):
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", a.slug):
        die("slug must be lowercase-kebab-case")
    if not is_game_repo() and not a.force:
        die("this is the clean Design Forge base; games don't live here.\n"
            "  Create a game repo instead:  python3 tools/forge.py spawn ../%s %s \"%s\"\n"
            "  (or pass --force to create a project in the base anyway, e.g. for testing)"
            % (a.slug, a.slug, a.name))
    dest = os.path.join(PROJECTS, a.slug)
    if os.path.exists(dest):
        die("project already exists: " + dest)
    shutil.copytree(TEMPLATE, dest)
    for p in md_files(dest):
        write(p, fill(read(p), NAME=a.name, SLUG=a.slug, DATE=today(), VERSION=platform_version()))
    # Seed task
    create_item(dest, "task", "ORC", "Run the Seed Interview and set up the project",
                tier="T1", phase="0", priority="blocking", creator="forge.py new",
                objective="Interview the Creative Owner using the Seed Interview in "
                          "platform/roles/orchestrator.md, fill PROJECT.md, then run "
                          "`forge.py decompose %s --max-phase 1`, set phase: 1 and regenerate the board." % a.slug,
                context=["[Orchestrator role](../../../platform/roles/orchestrator.md)",
                         "[Workflow](../../../platform/WORKFLOW.md)",
                         "[PROJECT.md](../PROJECT.md)"])
    build_board(dest)
    print("Created projects/%s. Next: an agent claims T-ORC-0001 (Seed Interview)." % a.slug)


def create_item(pdir, kind, code, title, tier="T2", needs=None, phase=None, priority="normal",
                coverage="", depends=None, parent="", creator="agent", objective="", context=None):
    code = code.upper()
    iid = next_id(pdir, kind, code)
    tpl = read(os.path.join(PLATFORM, "templates", kind + ".md"))
    text = fill(tpl, ID=iid, TITLE=title, ROLE=ROLES[code], DATE=today(),
                PHASE=phase if phase is not None else project_phase(pdir), CREATOR=creator)
    path = os.path.join(pdir, KINDS[kind][1], ("open" if kind == "question" else ""), iid + ".md")
    path = os.path.normpath(path)
    write(path, text)
    if kind == "task":
        set_fm(path, {"tier": tier, "needs": needs or [], "priority": priority,
                      "coverage": coverage, "depends_on": depends or [], "parent": parent})
        body = read(path)
        if objective:
            body = body.replace("<!-- One or two sentences: what will be true when this task is done? -->",
                                objective)
        if context:
            body = body.replace("- [AGENTS.md](../../../AGENTS.md)",
                                "- [AGENTS.md](../../../AGENTS.md)\n" + "\n".join("- " + c for c in context))
        write(path, body)
    elif kind == "question":
        set_fm(path, {"priority": priority})
    return iid, path


def cmd_id(a):
    print(next_id(project_dir(a.slug), a.kind, a.code))


def cmd_create(a):
    pdir = project_dir(a.slug)
    needs = [x for x in (a.needs or "").split(",") if x]
    bad = set(needs) - CAPS
    if bad:
        die("unknown capability flags: %s" % ", ".join(bad))
    if a.tier not in TIERS:
        die("tier must be T1, T2 or T3")
    iid, path = create_item(pdir, a.kind, a.code, a.title, tier=a.tier, needs=needs, phase=a.phase,
                            priority=a.priority, coverage=a.coverage or "",
                            depends=[x for x in (a.depends or "").split(",") if x],
                            parent=a.parent or "", creator=a.creator or "agent")
    print("%s  %s" % (iid, os.path.relpath(path, ROOT)))


def claimable(task_fm, tasks, agent_tier, caps, role, proj_phase, any_phase):
    """Return (ok, reason)."""
    if task_fm.get("status") != "open":
        return False, "status is " + str(task_fm.get("status"))
    for dep in task_fm.get("depends_on") or []:
        if dep not in tasks or tasks[dep][1].get("status") != "done":
            return False, "waiting on dependency " + dep
    t = task_fm.get("tier", "T2")
    if TIERS.get(agent_tier, 3) > TIERS.get(t, 2):
        return False, "needs tier %s" % t
    missing = [n for n in (task_fm.get("needs") or []) if n != "human" and n not in caps]
    if missing:
        return False, "missing capabilities: " + ", ".join(missing)
    if role and task_fm.get("role") != role and t != "T3":
        return False, "belongs to role " + str(task_fm.get("role"))
    try:
        ph = int(task_fm.get("phase") or 0)
    except ValueError:
        ph = 0
    if not any_phase and ph > proj_phase:
        return False, "phase %d not reached (project is in phase %d)" % (ph, proj_phase)
    return True, ""


def cmd_next(a):
    pdir = project_dir(a.slug)
    tasks = load_items(pdir, "task")
    caps = set(x for x in (a.caps or "").split(",") if x)
    phase = project_phase(pdir)
    found = []
    for tid, (p, fm) in tasks.items():
        ok, _ = claimable(fm, tasks, a.tier, caps, a.role, phase, a.any_phase)
        if ok:
            found.append((PRIORITIES.get(fm.get("priority"), 2), str(fm.get("phase")), tid, fm, p))
    found.sort(key=lambda x: (x[0], x[1], x[2]))
    if not found:
        print("No claimable tasks for tier %s%s. Check BOARD.md or ask the Orchestrator." %
              (a.tier, (" role " + a.role) if a.role else ""))
        return
    for _, _, tid, fm, p in found[: a.limit]:
        print("%-14s [%s %s p%s] %s  (%s)\n    %s" % (tid, fm.get("tier"), fm.get("priority"),
              fm.get("phase"), fm.get("title"), fm.get("role"), os.path.relpath(p, ROOT)))


def cmd_claim(a):
    pdir = project_dir(a.slug)
    tasks = load_items(pdir, "task")
    if a.id not in tasks:
        die("no task " + a.id)
    path, fm = tasks[a.id]
    caps = set(x for x in (a.caps or "").split(",") if x)
    ok, why = claimable(fm, tasks, a.tier, caps, a.role, project_phase(pdir), a.any_phase)
    if not ok:
        die("cannot claim %s: %s" % (a.id, why))
    who = "%s %s %s %s" % (a.agent, a.tier, a.role, now())
    set_fm(path, {"status": "claimed", "claimed_by": who})
    append_log(path, "%s | agent: %s  tier: %s  caps: [%s]  role: %s | claimed" %
               (now(), a.agent, a.tier, ", ".join(sorted(caps)), a.role))
    print("Claimed %s → %s" % (a.id, os.path.relpath(path, ROOT)))


def cmd_decompose(a):
    pdir = project_dir(a.slug)
    made = 0
    for row in coverage_rows(pdir):
        if a.discipline and row["discipline"] != a.discipline:
            continue
        if row["status"] != "stub" or row["ref"]:
            continue
        try:
            ph = int(row["phase"] or 0)
        except ValueError:
            ph = 0
        if a.max_phase is not None and ph > a.max_phase:
            continue
        code = ROLE_CODES.get(row["owner"])
        if not code:
            print("skip %s/%s: unknown owner %s" % (row["discipline"], row["key"], row["owner"]))
            continue
        title = "Resolve: " + row["topic"]
        if a.dry_run:
            print("[dry-run] %s %s/%s (%s, phase %d)" % (code, row["discipline"], row["key"], row["tier"], ph))
            continue
        iid, _ = create_item(
            pdir, "task", code, title, tier=row["tier"], needs=row["needs"], phase=str(ph),
            priority="high" if ph <= 1 else "normal",
            coverage="%s/%s" % (row["discipline"], row["key"]), creator="forge.py decompose",
            objective="Bring coverage item `%s` (%s) to `locked` or `n/a`. Interview the Creative "
                      "Owner as needed, record decisions, write the page(s), update the coverage row. "
                      "Split into child tasks if the topic is too large for one question batch."
                      % (row["key"], row["topic"]),
            context=["[Role: %s](../../../platform/roles/%s.md)" % (row["owner"], row["owner"]),
                     "[Discipline index](../wiki/%s/index.md)" % row["discipline"],
                     "[Vision](../wiki/00-vision/index.md)"])
        # rows are re-read every loop iteration via coverage_rows; write ref now
        set_row_cell(row, 7, iid)
        made += 1
    if not a.dry_run:
        build_board(pdir)
    print("Created %d task(s)." % made)


# ----------------------------------------------------------------- multi-product
def cmd_spawn(a):
    """Create a new game repo cloned from the clean base, with the base as `upstream`."""
    if is_game_repo():
        die("run spawn from the clean base repo, not from a game repo")
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", a.slug):
        die("slug must be lowercase-kebab-case")
    dest = os.path.abspath(a.dest)
    if os.path.exists(dest):
        die("destination already exists: " + dest)
    src = a.source or ROOT
    if src == ROOT:
        if not os.path.isdir(os.path.join(ROOT, ".git")):
            die("the base is not a git repo yet (git init + commit first)")
        if git("status", "--porcelain"):
            print("warning: the base has uncommitted changes; they will NOT be in the new game repo.")
    git("clone", src, dest, cwd=os.path.dirname(dest))
    git("remote", "rename", "origin", "upstream", cwd=dest)
    write(os.path.join(dest, ".forge-game"),
          "# Marks this repository as a Design Forge GAME repo (not the clean base).\n"
          "# Platform updates: python3 tools/forge.py upgrade\n"
          "upstream: %s\nspawned: %s\nplatform_version: %s\n" % (src, today(), platform_version()))
    r = subprocess.run([sys.executable, os.path.join(dest, "tools", "forge.py"), "new", a.slug, a.name],
                       capture_output=True, text=True)
    if r.returncode != 0:
        die(r.stderr.strip())
    git("add", "-A", cwd=dest)
    c = subprocess.run(["git", "commit", "-q", "-m", "Create game project %s (Design Forge %s)"
                        % (a.slug, platform_version())], cwd=dest, capture_output=True, text=True)
    print("Game repo created: %s" % dest)
    print("  project:  projects/%s" % a.slug)
    print("  upstream: %s  (pull platform updates with: python3 tools/forge.py upgrade)" % src)
    if c.returncode != 0:
        print("  note: initial commit skipped (%s). Commit manually." % (c.stderr.strip().split("\n")[0]))
    print("Next: open an agent in that folder: \"Read AGENTS.md. You are the Orchestrator (T1). "
          "Run the Seed Interview for projects/%s.\"" % a.slug)


def sync_coverage(pdir):
    """Bring a project's structure up to date with the template without touching its content:
    adds missing discipline folders, missing coverage rows, and missing template files."""
    changes = []
    slug = os.path.basename(pdir)
    pfm = parse_fm(read(os.path.join(pdir, "PROJECT.md"))) or {}
    kw = dict(NAME=pfm.get("name", slug), SLUG=slug, DATE=today(), VERSION=platform_version())
    # 1. missing files / folders
    for src in md_files(TEMPLATE) + [os.path.join(dp, f) for dp, _, fs in os.walk(TEMPLATE)
                                     for f in fs if f == ".gitkeep"]:
        rel = os.path.relpath(src, TEMPLATE)
        dst = os.path.join(pdir, rel)
        if rel in ("PROJECT.md",) or os.path.exists(dst):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        write(dst, fill(read(src), **kw) if src.endswith(".md") else "")
        changes.append("added " + rel)
    # 2. missing coverage rows in existing indexes
    have = set((r["discipline"], r["key"]) for r in coverage_rows(pdir))
    for row in coverage_rows(TEMPLATE):
        if (row["discipline"], row["key"]) in have:
            continue
        path = os.path.join(pdir, "wiki", row["discipline"], "index.md")
        lines = read(path).split("\n")
        last = max([i for i, l in enumerate(lines) if l.startswith("|")] or [len(lines) - 1])
        lines.insert(last + 1, "| `%s` | %s | %s | %s | %s | stub | | |" %
                     (row["key"], row["topic"], row["tier"], ", ".join(row["needs"]), row["phase"]))
        write(path, "\n".join(lines))
        changes.append("added coverage row %s/%s" % (row["discipline"], row["key"]))
    return changes


def cmd_sync(a):
    targets = game_projects() if (a.slug == "--all" or a.all) else [project_dir(a.slug)]
    for pdir in targets:
        ch = sync_coverage(pdir)
        set_fm(os.path.join(pdir, "PROJECT.md"), {"platform_version": platform_version()})
        build_board(pdir)
        print("== %s: %d change(s)" % (os.path.basename(pdir), len(ch)))
        for c in ch:
            print("   " + c)


def cmd_upgrade(a):
    """Pull the latest platform from `upstream` into this game repo, then sync every project."""
    if not is_game_repo():
        die("upgrade runs inside a game repo (this is the clean base)")
    if git("status", "--porcelain"):
        die("working tree not clean; commit or stash first")
    head = git("ls-remote", "--symref", "upstream", "HEAD")
    m = re.search(r"ref: refs/heads/(\S+)\s+HEAD", head)
    branch = a.branch or (m.group(1) if m else "main")
    before = platform_version()
    git("fetch", "upstream")
    r = subprocess.run(["git", "merge", "--no-edit", "upstream/" + branch], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        die("merge conflict pulling the platform. Usually caused by editing platform/ or "
            "projects/_template/ in this game repo. Resolve, commit, then run `forge.py sync`.\n"
            + r.stdout + r.stderr)
    after = platform_version()
    print("Platform %s → %s" % (before, after))
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "forge.py"), "sync"])
    print("Review the changes (see CHANGELOG.md), then commit.")


# ----------------------------------------------------------------- validate
def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"`[^`]*`", "", text)


def check_links(path, text, errors):
    for target in LINK_RE.findall(strip_code_blocks_only(text)):
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        t = target.split("#")[0]
        if not t:
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), t))):
            errors.append((path, "broken link → " + target))


def strip_code_blocks_only(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def validate_project(pdir):
    E, W = [], []
    tasks = load_items(pdir, "task")
    qs = load_items(pdir, "question")
    ds = load_items(pdir, "decision")
    is_template = os.path.basename(pdir) == "_template"
    cov_keys = set("%s/%s" % (r["discipline"], r["key"]) for r in coverage_rows(pdir))

    for kind, items in (("task", tasks), ("question", qs), ("decision", ds)):
        for iid, (p, fm) in items.items():
            if os.path.splitext(os.path.basename(p))[0] != iid:
                E.append((p, "file name does not match id %s" % iid))
            if not ID_RE.match(iid):
                E.append((p, "malformed id %s" % iid))
            if fm.get("role") not in ROLE_CODES:
                E.append((p, "unknown role '%s'" % fm.get("role")))

    for tid, (p, fm) in tasks.items():
        st = fm.get("status")
        if st not in TASK_STATUSES:
            E.append((p, "bad status '%s'" % st))
        if fm.get("tier") not in TIERS:
            E.append((p, "bad tier '%s'" % fm.get("tier")))
        for n in fm.get("needs") or []:
            if n not in CAPS:
                E.append((p, "unknown capability '%s'" % n))
        for dep in fm.get("depends_on") or []:
            if dep not in tasks:
                E.append((p, "depends_on unknown task " + dep))
        if fm.get("parent") and fm["parent"] not in tasks:
            E.append((p, "parent unknown task " + fm["parent"]))
        if fm.get("coverage") and fm["coverage"] not in cov_keys:
            E.append((p, "coverage key not in any index: " + fm["coverage"]))
        for q in fm.get("questions") or []:
            if q not in qs:
                E.append((p, "unknown question batch " + q))
        if st == "waiting" and not fm.get("questions"):
            E.append((p, "status waiting but no questions listed"))
        if st == "claimed" and not fm.get("claimed_by"):
            E.append((p, "claimed but claimed_by empty"))
        if st == "blocked" and "blocked_reason" not in fm:
            W.append((p, "blocked without blocked_reason"))

    for qid, (p, fm) in qs.items():
        st = fm.get("status")
        if st not in Q_STATUSES:
            E.append((p, "bad status '%s'" % st))
        in_open = os.sep + "open" + os.sep in p
        if st == "processed" and in_open:
            E.append((p, "processed batch still in questions/open/"))
        if st in ("open", "answered") and not in_open:
            E.append((p, "unprocessed batch outside questions/open/"))
        for t in fm.get("tasks") or []:
            if t not in tasks:
                E.append((p, "unknown task " + t))

    for did, (p, fm) in ds.items():
        st = fm.get("status")
        if st not in D_STATUSES:
            E.append((p, "bad status '%s'" % st))
        if st in ("locked", "superseded"):
            if fm.get("source") not in ("owner", "delegated"):
                E.append((p, "locked decision needs source owner|delegated"))
            qref = str(fm.get("question") or "").split("#")[0]
            if not qref:
                E.append((p, "locked decision has no question reference"))
            elif qref not in qs:
                E.append((p, "question %s not found" % qref))
        if st == "superseded" and not fm.get("superseded_by"):
            E.append((p, "superseded without superseded_by"))
        for ref in ("supersedes", "superseded_by"):
            if fm.get(ref) and fm[ref] not in ds:
                E.append((p, "%s points to unknown %s" % (ref, fm[ref])))
        body = split_fm(read(p))[1]
        m = re.search(r"## Decision\s*\n(.*?)(\n## |\Z)", body, re.S)
        if st == "locked" and m and HEDGE_RE.search(strip_code(m.group(1))):
            E.append((p, "hedge word in ## Decision: '%s'" % HEDGE_RE.search(strip_code(m.group(1))).group(0)))

    for p in md_files(os.path.join(pdir, "wiki")):
        text = read(p)
        fm = parse_fm(text)
        if fm is None:
            E.append((p, "missing frontmatter"))
            continue
        for k in ("title", "owner", "status"):
            if not fm.get(k):
                E.append((p, "frontmatter missing '%s'" % k))
        st = fm.get("status")
        if st not in PAGE_STATUSES:
            E.append((p, "bad status '%s'" % st))
        for d in fm.get("decisions") or []:
            if d not in ds:
                E.append((p, "cites unknown decision " + d))
            elif ds[d][1].get("status") == "superseded":
                W.append((p, "cites superseded decision " + d))
        body = split_fm(text)[1]
        if st == "locked":
            for n, line in enumerate(strip_code(body).split("\n"), 1):
                m = HEDGE_RE.search(line)
                if m:
                    E.append((p, "hedge word '%s' in locked page (body line %d)" % (m.group(0), n)))
            if re.search(r"^## Open questions", body, re.M):
                E.append((p, "locked page still has '## Open questions'"))
            if not fm.get("decisions") and not p.endswith("index.md"):
                W.append((p, "locked page cites no decisions"))
            if fm.get("guide") is True and "## Player-facing explanation" not in body:
                E.append((p, "guide page lacks '## Player-facing explanation'"))

    for r in coverage_rows(pdir):
        where = "%s (row `%s`)" % (r["path"], r["key"])
        if r["status"] not in PAGE_STATUSES:
            E.append((where, "bad coverage status '%s'" % r["status"]))
        if r["tier"] not in TIERS:
            E.append((where, "bad tier '%s'" % r["tier"]))
        refs = re.findall(r"[TQD]-[A-Z]+-\d{4}", r["ref"])
        for ref in refs:
            pool = {"T": tasks, "Q": qs, "D": ds}[ref[0]]
            if ref not in pool:
                E.append((where, "ref %s does not exist" % ref))
        if r["status"] in ("locked", "n/a") and not any(x.startswith("D-") for x in refs):
            E.append((where, "%s row must reference a decision (D-*)" % r["status"]))
        if r["status"] == "locked" and not r["page"]:
            E.append((where, "locked row has no page"))

    for p in md_files(pdir):
        check_links(p, read(p), E)

    if not is_template:
        for p in md_files(pdir):
            if "{{" in read(p) and "}}" in read(p):
                W.append((p, "unfilled template placeholder"))
    return E, W


def cmd_validate(a):
    targets = []
    if a.slug == "--all" or a.all:
        targets = [os.path.join(PROJECTS, d) for d in sorted(os.listdir(PROJECTS))
                   if os.path.isdir(os.path.join(PROJECTS, d))]
    else:
        targets = [project_dir(a.slug)]
    total_e = 0
    pe = []
    for p in md_files(PLATFORM) + [os.path.join(ROOT, f) for f in ("AGENTS.md", "README.md")]:
        if os.path.exists(p) and os.sep + "templates" + os.sep not in p:  # template links resolve only once copied
            check_links(p, read(p), pe)
    for path, msg in pe:
        print("ERROR  %s: %s" % (os.path.relpath(path, ROOT), msg))
    total_e += len(pe)
    for t in targets:
        E, W = validate_project(t)
        print("== %s: %d error(s), %d warning(s)" % (os.path.basename(t), len(E), len(W)))
        for path, msg in E:
            print("ERROR  %s: %s" % (path.replace(ROOT + os.sep, ""), msg))
        for path, msg in W:
            print("warn   %s: %s" % (path.replace(ROOT + os.sep, ""), msg))
        total_e += len(E)
    sys.exit(1 if total_e else 0)


# ----------------------------------------------------------------- board
def build_board(pdir):
    fm = parse_fm(read(os.path.join(pdir, "PROJECT.md"))) or {}
    phase = project_phase(pdir)
    tasks = load_items(pdir, "task")
    qs = load_items(pdir, "question")
    ds = load_items(pdir, "decision")
    rows = coverage_rows(pdir)
    L = ["<!-- GENERATED by tools/forge.py board — do not edit by hand -->", "",
         "# Board — %s" % fm.get("name", os.path.basename(pdir)), "",
         "**Phase:** %d · **Updated:** %s · **Decisions:** %d locked" %
         (phase, now(), sum(1 for _, f in ds.values() if f.get("status") == "locked")), ""]

    # Coverage
    done_total = sum(1 for r in rows if r["status"] in ("locked", "n/a"))
    pct = (100 * done_total // len(rows)) if rows else 0
    L += ["## Coverage — %d / %d resolved (%d%%)" % (done_total, len(rows), pct), "",
          "| discipline | resolved | locked | n/a | draft | exploring | stub | progress |",
          "|---|---|---|---|---|---|---|---|"]
    for d in disciplines(pdir):
        rs = [r for r in rows if r["discipline"] == d]
        c = {s: sum(1 for r in rs if r["status"] == s) for s in PAGE_STATUSES}
        res = c["locked"] + c["n/a"]
        bar = "█" * (10 * res // len(rs) if rs else 0)
        L.append("| [%s](wiki/%s/index.md) | %d/%d | %d | %d | %d | %d | %d | `%-10s` |" %
                 (d, d, res, len(rs), c["locked"], c["n/a"], c["draft"], c["exploring"], c["stub"], bar))
    L.append("")

    # Questions waiting on the owner
    open_qs = [(PRIORITIES.get(f.get("priority"), 2), i, f, p) for i, (p, f) in qs.items()
               if f.get("status") == "open"]
    answered = [(i, f, p) for i, (p, f) in qs.items() if f.get("status") == "answered"]
    L += ["## Waiting on the Creative Owner (%d batch(es))" % len(open_qs), ""]
    for _, i, f, p in sorted(open_qs, key=lambda x: (x[0], x[1])):
        L.append("- **[%s](%s)** (%s): %s" % (i, os.path.relpath(p, pdir), f.get("priority"), f.get("title")))
    if not open_qs:
        L.append("_Nothing — the team is not waiting on you._")
    if answered:
        L += ["", "**Answered, awaiting intake:** " +
              ", ".join("[%s](%s)" % (i, os.path.relpath(p, pdir)) for i, f, p in answered)]
    L.append("")

    # Tasks
    by = {}
    for tid, (p, f) in tasks.items():
        by.setdefault(f.get("status", "?"), []).append((tid, f, p))
    L += ["## Tasks", "",
          " · ".join("%s: %d" % (s, len(by.get(s, []))) for s in
                     ("open", "claimed", "waiting", "blocked", "review", "done", "cancelled")), ""]
    for s, label in (("blocked", "Blocked"), ("review", "In review"), ("claimed", "In progress"),
                     ("waiting", "Waiting on answers")):
        if by.get(s):
            L += ["### " + label, "", "| id | title | role | tier | note |", "|---|---|---|---|---|"]
            for tid, f, p in sorted(by[s], key=lambda x: x[0]):
                note = f.get("blocked_reason", "") if s == "blocked" else (
                    f.get("claimed_by", "") if s == "claimed" else ", ".join(f.get("questions") or []))
                L.append("| [%s](%s) | %s | %s | %s | %s |" % (tid, os.path.relpath(p, pdir), f.get("title"),
                         f.get("role"), f.get("tier"), note))
            L.append("")

    # Claimable by tier
    L += ["### Claimable now, by agent tier", "", "| agent tier | claimable tasks |", "|---|---|"]
    for t in ("T1", "T2", "T3"):
        n = sum(1 for _, (p, f) in tasks.items()
                if claimable(f, tasks, t, CAPS, None, phase, False)[0])
        L.append("| %s | %d |" % (t, n))
    L += ["", "_Get yours with_ `python3 tools/forge.py next %s --tier <T1|T2|T3>`" % os.path.basename(pdir), ""]
    write(os.path.join(pdir, "BOARD.md"), "\n".join(L))


def cmd_board(a):
    pdir = project_dir(a.slug)
    build_board(pdir)
    print("Wrote " + os.path.relpath(os.path.join(pdir, "BOARD.md"), ROOT))


# ----------------------------------------------------------------- guide
def cmd_guide(a):
    pdir = project_dir(a.slug)
    fm_p = parse_fm(read(os.path.join(pdir, "PROJECT.md"))) or {}
    L = ["<!-- GENERATED by tools/forge.py guide — do not edit by hand -->", "",
         "# %s — Compiled Guide Source" % fm_p.get("name", a.slug), "",
         "Assembled from every `guide: true` + `status: locked` page. The Guide Writer turns "
         "this into the finished guide.", ""]
    count = 0
    for p in md_files(os.path.join(pdir, "wiki")):
        text = read(p)
        fm = parse_fm(text) or {}
        if fm.get("guide") is True and fm.get("status") == "locked":
            body = split_fm(text)[1]
            m = re.search(r"## Player-facing explanation\s*\n(.*?)(\n## |\Z)", body, re.S)
            content = m.group(1).strip() if m else body.strip()
            rel = os.path.relpath(p, os.path.join(pdir, "guide"))
            L += ["## %s" % fm.get("title"), "", "_Source: [%s](%s)_" % (os.path.relpath(p, pdir), rel), "",
                  content, ""]
            count += 1
    write(os.path.join(pdir, "guide", "_compiled.md"), "\n".join(L))
    print("Compiled %d page(s) into %s" % (count, os.path.relpath(os.path.join(pdir, "guide", "_compiled.md"), ROOT)))


# ----------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Design Forge CLI. See AGENTS.md.")
    sp = ap.add_subparsers(dest="cmd")

    p = sp.add_parser("new"); p.add_argument("slug"); p.add_argument("name")
    p.add_argument("--force", action="store_true"); p.set_defaults(f=cmd_new)
    p = sp.add_parser("spawn"); p.add_argument("dest"); p.add_argument("slug"); p.add_argument("name")
    p.add_argument("--source", help="base repo path or URL (default: this repo)"); p.set_defaults(f=cmd_spawn)
    p = sp.add_parser("upgrade"); p.add_argument("--branch"); p.set_defaults(f=cmd_upgrade)
    p = sp.add_parser("sync"); p.add_argument("slug", nargs="?", default="--all")
    p.add_argument("--all", action="store_true"); p.set_defaults(f=cmd_sync)
    p = sp.add_parser("list"); p.set_defaults(f=cmd_list)
    p = sp.add_parser("board"); p.add_argument("slug"); p.set_defaults(f=cmd_board)

    p = sp.add_parser("next"); p.add_argument("slug"); p.add_argument("--tier", required=True, choices=list(TIERS))
    p.add_argument("--caps", default=""); p.add_argument("--role"); p.add_argument("--limit", type=int, default=10)
    p.add_argument("--any-phase", action="store_true"); p.set_defaults(f=cmd_next)

    p = sp.add_parser("claim"); p.add_argument("slug"); p.add_argument("id")
    p.add_argument("--agent", required=True); p.add_argument("--tier", required=True, choices=list(TIERS))
    p.add_argument("--role", required=True); p.add_argument("--caps", default="")
    p.add_argument("--any-phase", action="store_true"); p.set_defaults(f=cmd_claim)

    p = sp.add_parser("id"); p.add_argument("slug"); p.add_argument("kind", choices=list(KINDS))
    p.add_argument("code"); p.set_defaults(f=cmd_id)

    p = sp.add_parser("create"); p.add_argument("slug"); p.add_argument("kind", choices=list(KINDS))
    p.add_argument("code"); p.add_argument("title"); p.add_argument("--tier", default="T2")
    p.add_argument("--needs", default=""); p.add_argument("--phase"); p.add_argument("--priority", default="normal",
                   choices=list(PRIORITIES)); p.add_argument("--coverage"); p.add_argument("--depends")
    p.add_argument("--parent"); p.add_argument("--creator"); p.set_defaults(f=cmd_create)

    p = sp.add_parser("decompose"); p.add_argument("slug"); p.add_argument("--max-phase", type=int)
    p.add_argument("--discipline"); p.add_argument("--dry-run", action="store_true"); p.set_defaults(f=cmd_decompose)

    p = sp.add_parser("validate"); p.add_argument("slug", nargs="?", default="--all")
    p.add_argument("--all", action="store_true"); p.set_defaults(f=cmd_validate)

    p = sp.add_parser("guide"); p.add_argument("slug"); p.set_defaults(f=cmd_guide)

    a = ap.parse_args()
    if not getattr(a, "f", None):
        ap.print_help()
        return
    a.f(a)


if __name__ == "__main__":
    main()
