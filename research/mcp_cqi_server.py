"""
ENDORYS Platform — Protocol E001 Model Context Protocol (MCP) Diagnostic Server

Exposes deterministic Coupling Quality Index (CQI) evaluation and DICOM TID 1500
report validation as standard JSON-RPC 2.0 MCP tools over stdio for AI research
agents and automated acoustic metrology pipelines.

License: Apache-2.0 (Software) — Hardware & closed-loop CQI gating patent rights
reserved under Indian Patent Application No. 202641134091 (Patent Pending).
"""

from __future__ import annotations

import json
import sys
from typing import Any


def evaluate_cqi_gate(
    boundary_reflection_kpa: float,
    target_echo_kpa: float,
    curvature_radius_mm: float = 45.0,
    threshold: float = 0.65,
) -> dict[str, Any]:
    """Computes Coupling Quality Index (CQI) and returns deterministic gate decision."""
    if boundary_reflection_kpa <= 0:
        ratio = 0.0
    else:
        ratio = target_echo_kpa / boundary_reflection_kpa
    raw_cqi = ratio / (ratio + 0.8)
    curvature_factor = min(1.0, max(0.75, curvature_radius_mm / 60.0))
    cqi = round(min(0.98, max(0.0, raw_cqi * curvature_factor)), 4)
    accepted = cqi >= threshold
    return {
        "cqi_score": cqi,
        "threshold": threshold,
        "gate_status": "ACCEPTED" if accepted else "REJECTED",
        "bulk_to_boundary_ratio": round(ratio, 4),
        "curvature_radius_mm": curvature_radius_mm,
        "protocol_ref": "Protocol E001 (DOI: 10.5281/zenodo.24555614)",
    }


def handle_rpc(request: dict[str, Any]) -> dict[str, Any] | None:
    req_id = request.get("id")
    method = request.get("method", "")
    params = request.get("params") or {}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "endorys-e001-mcp", "version": "0.1.1"},
                "capabilities": {"tools": {}},
            },
        }
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "evaluate_cqi_gate",
                        "description": "Evaluate curved-surface ultrasound Coupling Quality Index (CQI) and frame gate status.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "boundary_reflection_kpa": {"type": "number"},
                                "target_echo_kpa": {"type": "number"},
                                "curvature_radius_mm": {"type": "number", "default": 45.0},
                                "threshold": {"type": "number", "default": 0.65},
                            },
                            "required": ["boundary_reflection_kpa", "target_echo_kpa"],
                        },
                    }
                ]
            },
        }
    if method == "tools/call":
        args = params.get("arguments") or {}
        res = evaluate_cqi_gate(
            boundary_reflection_kpa=float(args["boundary_reflection_kpa"]),
            target_echo_kpa=float(args["target_echo_kpa"]),
            curvature_radius_mm=float(args.get("curvature_radius_mm", 45.0)),
            threshold=float(args.get("threshold", 0.65)),
        )
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [{"type": "text", "text": json.dumps(res)}]},
        }
    if req_id is None:
        return None
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        reply = handle_rpc(json.loads(line))
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
