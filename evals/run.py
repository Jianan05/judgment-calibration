"""Run small paired tests against an already installed Skill. Uses account quota."""
import argparse
import json
import pathlib
import shutil
import subprocess
import tomllib

ROOT = pathlib.Path(__file__).resolve().parents[1]

def disable_override(skill):
    cfg = pathlib.Path.home() / ".codex/config.toml"
    data = tomllib.loads(cfg.read_text(encoding="utf-8")) if cfg.exists() else {}
    entries = [e for e in data.get("skills", {}).get("config", [])
               if pathlib.Path(e["path"]).resolve() != skill.resolve()]
    entries.append({"path": str(skill.resolve()), "enabled": False})
    return "skills.config=[" + ",".join(
        "{path=" + json.dumps(e["path"]) + ",enabled=" + str(e.get("enabled", True)).lower() + "}"
        for e in entries) + "]"

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-path", type=pathlib.Path, required=True,
                        help="Absolute path of the installed SKILL.md")
    parser.add_argument("--case", required=True, help="One case ID from cases.json")
    parser.add_argument("--mode", choices=["skill", "baseline", "both"], default="both")
    parser.add_argument("--output", type=pathlib.Path, default=ROOT / "local-results")
    args = parser.parse_args()
    cli = shutil.which("codex")
    if not cli or not args.skill_path.is_file():
        parser.error("Codex CLI and an installed Skill are required")
    cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))
    case = next((c for c in cases if c["id"] == args.case), None)
    if not case:
        parser.error("Unknown case ID")
    args.output.mkdir(parents=True, exist_ok=True)
    workspace = args.output / "workspace"
    workspace.mkdir(exist_ok=True)
    modes = ["skill", "baseline"] if args.mode == "both" else [args.mode]
    for mode in modes:
        stem = args.output / (case["id"] + "-" + mode)
        cmd = [cli, "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "read-only",
               "-c", 'approval_policy="never"', "--json", "-o", str(stem.with_suffix(".txt").resolve())]
        if mode == "baseline":
            cmd += ["-c", disable_override(args.skill_path)]
        cmd.append(case["prompt"])
        result = subprocess.run(cmd, cwd=workspace, capture_output=True,
                                encoding="utf-8", errors="replace", timeout=300)
        stem.with_suffix(".jsonl").write_text(result.stdout, encoding="utf-8")
        stem.with_suffix(".stderr.txt").write_text(result.stderr, encoding="utf-8")
        print(case["id"], mode, "exit_code=", result.returncode)
        if result.returncode:
            raise SystemExit(result.returncode)

if __name__ == "__main__":
    main()
