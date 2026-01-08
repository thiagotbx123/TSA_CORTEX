#!/usr/bin/env python3
"""
SpineHUB Python Bridge - JSON-based IPC handler for TypeScript integration.

This bridge enables TSA_CORTEX (TypeScript) to call SpineHUB (Python) modules
via subprocess with JSON-based communication.

Usage:
    echo '{"method": "analyzers.check_tools", "params": {}}' | python bridge.py
"""

import json
import sys
import time
import traceback
from pathlib import Path
from typing import Any, Dict

# Add current directory to path for local imports
BRIDGE_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(BRIDGE_ROOT))

# Also add SpineHUB root if available (for development)
SPINEHUB_ROOT = Path("C:/Users/adm_r/SpineHUB")
if SPINEHUB_ROOT.exists():
    sys.path.insert(0, str(SPINEHUB_ROOT))
    sys.path.insert(0, str(SPINEHUB_ROOT / "src"))
    sys.path.insert(0, str(SPINEHUB_ROOT / "modules"))


def handle_analyzers(method: str, params: Dict[str, Any]) -> Any:
    """Handle analyzer-related calls."""
    from analyzers.code_analyzer import CodeAnalyzer

    project_path = params.get("project_path", ".")
    analyzer = CodeAnalyzer(Path(project_path))

    if method == "analyzers.check_tools":
        return analyzer.check_tools()

    elif method == "analyzers.run_all":
        paths = params.get("paths")
        result = analyzer.run_all(paths)
        return {
            "results": {k: _serialize_analyzer_result(v) for k, v in result.items()},
            "total_issues": sum(len(r.issues) for r in result.values()),
            "has_errors": any(
                any(i.severity.value == "error" for i in r.issues)
                for r in result.values()
            ),
            "has_security_issues": any(
                any(i.severity.value == "security" for i in r.issues)
                for r in result.values()
            ),
        }

    elif method == "analyzers.run_single":
        tool = params.get("tool", "ruff")
        paths = params.get("paths")
        result = analyzer.run_single(tool, paths)
        return _serialize_analyzer_result(result)

    raise ValueError(f"Unknown analyzer method: {method}")


def handle_quality(method: str, params: Dict[str, Any]) -> Any:
    """Handle quality validation calls."""
    from spinehub.benchmark import QualityValidator

    validator = QualityValidator()

    if method == "quality.validate":
        content = params["content"]
        passed, report = validator.validate(content)
        return {
            "passed": passed,
            "score": report.score,
            "status": "PASS" if passed else "FAIL",
            "errors": report.errors,
            "warnings": report.warnings,
            "info": report.info,
            "report": validator.format_report(report),
        }

    elif method == "quality.validate_file":
        file_path = Path(params["file_path"])
        content = file_path.read_text(encoding="utf-8")
        passed, report = validator.validate(content)
        return {
            "passed": passed,
            "score": report.score,
            "status": "PASS" if passed else "FAIL",
            "errors": report.errors,
            "warnings": report.warnings,
            "info": report.info,
            "report": validator.format_report(report),
            "file": str(file_path),
        }

    raise ValueError(f"Unknown quality method: {method}")


def handle_credentials(method: str, params: Dict[str, Any]) -> Any:
    """Handle credentials management calls."""
    from credentials.manager import CredentialsManager

    cm = CredentialsManager()

    if method == "credentials.status":
        return cm.get_all_status()

    elif method == "credentials.mcp_status":
        return cm.get_mcp_status()

    elif method == "credentials.copy":
        target = Path(params["target"])
        services = params.get("services")
        return cm.copy_to_project(target, services)

    elif method == "credentials.get":
        key = params["key"]
        return {"key": key, "value": cm.get(key), "exists": cm.has(key)}

    raise ValueError(f"Unknown credentials method: {method}")


def handle_linear(method: str, params: Dict[str, Any]) -> Any:
    """Handle Linear template/generator calls."""
    from linear.templates import (
        DEFAULT_TEMPLATES, get_template, list_templates,
        apply_template_variables, IssueTemplate
    )

    if method == "linear.list_templates":
        return [_serialize_template(t) for t in list_templates()]

    elif method == "linear.get_template":
        template = get_template(params["template_id"])
        return _serialize_template(template) if template else None

    elif method == "linear.apply_template":
        template = get_template(params["template_id"])
        if not template:
            raise ValueError(f"Template not found: {params['template_id']}")

        variables = params.get("variables", {})
        title = apply_template_variables(template.title_pattern, variables)
        body = apply_template_variables(template.body_template, variables)
        return {
            "title": title,
            "body": body,
            "labels": template.labels,
            "priority": template.priority,
        }

    raise ValueError(f"Unknown linear method: {method}")


def handle_privacy(method: str, params: Dict[str, Any]) -> Any:
    """Handle privacy/PII redaction calls."""
    from utils.privacy import redact_pii, RedactionConfig

    if method == "privacy.redact":
        config_dict = params.get("config", {})
        config = RedactionConfig(**config_dict)
        result = redact_pii(params["text"], config)
        return {
            "text": result.text,
            "redacted_count": result.redacted_count,
            "types": result.types,
        }

    elif method == "privacy.redact_batch":
        config_dict = params.get("config", {})
        config = RedactionConfig(**config_dict)
        results = []
        for text in params["texts"]:
            result = redact_pii(text, config)
            results.append({
                "text": result.text,
                "redacted_count": result.redacted_count,
                "types": result.types,
            })
        return results

    raise ValueError(f"Unknown privacy method: {method}")


def handle_datetime(method: str, params: Dict[str, Any]) -> Any:
    """Handle datetime utility calls."""
    from utils.datetime_utils import (
        get_default_date_range, parse_date_range, format_local_time,
        slack_ts_to_date, date_to_slack_ts, now_brasil, format_display
    )

    if method == "datetime.default_range":
        dr = get_default_date_range(
            params.get("timezone", "America/Sao_Paulo"),
            params.get("days", 7)
        )
        return {
            "start": dr.start.isoformat(),
            "end": dr.end.isoformat(),
            "timezone": dr.timezone
        }

    elif method == "datetime.parse_range":
        dr = parse_date_range(
            params.get("start"),
            params.get("end"),
            params.get("timezone", "America/Sao_Paulo"),
            params.get("default_days", 7)
        )
        return {
            "start": dr.start.isoformat(),
            "end": dr.end.isoformat(),
            "timezone": dr.timezone
        }

    elif method == "datetime.now_brasil":
        now = now_brasil()
        return {
            "iso": now.isoformat(),
            "display": format_display(now),
            "unix": int(now.timestamp())
        }

    elif method == "datetime.slack_to_date":
        ts = params["ts"]
        dt = slack_ts_to_date(ts)
        return {
            "iso": dt.isoformat(),
            "display": format_display(dt),
            "unix": int(dt.timestamp())
        }

    raise ValueError(f"Unknown datetime method: {method}")


def handle_slack(method: str, params: Dict[str, Any]) -> Any:
    """Handle Slack channel mapper calls."""
    from utils.slack_channels import SlackChannelMapper, ChannelInfo

    mapper = SlackChannelMapper(
        token=params.get("token"),
        company_domain=params.get("company_domain", "@testbox.com"),
        channel_prefixes=params.get("channel_prefixes")
    )

    if method == "slack.list_channels":
        prefixes = params.get("prefixes")
        channels = mapper.list_channels(prefixes)
        return [
            {
                "id": c.id,
                "name": c.name,
                "is_private": c.is_private,
                "num_members": c.num_members
            }
            for c in channels
        ]

    elif method == "slack.map_channel":
        channel_data = params["channel"]
        channel = ChannelInfo(**channel_data)
        mapping = mapper.map_channel(channel)
        return {
            "channel": mapping.channel,
            "channel_id": mapping.channel_id,
            "tsa_members": mapping.tsa_members,
            "eng_members": mapping.eng_members,
            "gtm_members": mapping.gtm_members,
            "external_members": mapping.external_members,
        }

    elif method == "slack.get_user_role":
        name = params["name"]
        return {"name": name, "role": mapper.get_user_role(name)}

    raise ValueError(f"Unknown slack method: {method}")


# Serialization helpers
def _serialize_analyzer_result(result) -> Dict[str, Any]:
    """Serialize AnalyzerResult to dict."""
    return {
        "tool": result.tool,
        "success": result.success,
        "issues": [_serialize_issue(i) for i in result.issues],
        "summary": result.summary,
        "raw_output": result.raw_output,
        "error": result.error,
    }


def _serialize_issue(issue) -> Dict[str, Any]:
    """Serialize Issue to dict."""
    return {
        "file": issue.file,
        "line": issue.line,
        "column": issue.column,
        "code": issue.code,
        "message": issue.message,
        "severity": issue.severity.value,
        "tool": issue.tool,
        "fix_available": issue.fix_available,
        "fix_description": issue.fix_description,
    }


def _serialize_template(template) -> Dict[str, Any]:
    """Serialize IssueTemplate to dict."""
    return {
        "id": template.id,
        "name": template.name,
        "description": template.description,
        "title_pattern": template.title_pattern,
        "body_template": template.body_template,
        "labels": template.labels,
        "priority": template.priority,
        "default_assignee": template.default_assignee,
        "estimate_points": template.estimate_points,
    }


# Handler dispatch table
HANDLERS = {
    "analyzers": handle_analyzers,
    "quality": handle_quality,
    "credentials": handle_credentials,
    "linear": handle_linear,
    "privacy": handle_privacy,
    "datetime": handle_datetime,
    "slack": handle_slack,
}


def main():
    """Main entry point for bridge."""
    start_time = time.time()

    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            raise ValueError("No input provided")

        request = json.loads(input_data)

        method = request.get("method")
        params = request.get("params", {})

        if not method:
            raise ValueError("No method specified")

        # Route to handler based on module prefix
        module = method.split(".")[0]
        handler = HANDLERS.get(module)

        if not handler:
            raise ValueError(f"Unknown module: {module}. Available: {list(HANDLERS.keys())}")

        result = handler(method, params)

        response = {
            "success": True,
            "data": result,
            "execution_time_ms": int((time.time() - start_time) * 1000)
        }

    except Exception as e:
        response = {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc(),
            "execution_time_ms": int((time.time() - start_time) * 1000)
        }

    # Output JSON response
    print(json.dumps(response, default=str, ensure_ascii=False))


if __name__ == "__main__":
    main()
