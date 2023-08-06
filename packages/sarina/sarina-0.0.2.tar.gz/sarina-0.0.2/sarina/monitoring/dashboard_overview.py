import json

dashboard = json.dumps(
    {
        "annotations": {
            "list": [
                {
                    "builtIn": 1,
                    "datasource": {"type": "grafana", "uid": "-- Grafana --"},
                    "enable": True,
                    "hide": True,
                    "iconColor": "rgba(0, 211, 255, 1)",
                    "name": "Annotations & Alerts",
                    "target": {
                        "limit": 100,
                        "matchAny": False,
                        "tags": [],
                        "type": "dashboard",
                    },
                    "type": "dashboard",
                }
            ]
        },
        "editable": True,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 0,
        "id": 4,
        "links": [],
        "liveNow": False,
        "panels": [
            {
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-green", "value": None}],
                        },
                        "unit": "Bps",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 0, "y": 0},
                "id": 16,
                "options": {
                    "colorMode": "background",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "targets": [
                    {
                        "expr": 'sum(rate(proxy_downstream_total{job="sarina-server"}[5m]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Global Downstream",
                "type": "stat",
            },
            {
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-blue", "value": None}],
                        },
                        "unit": "Bps",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 5, "y": 0},
                "id": 18,
                "options": {
                    "colorMode": "background",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "targets": [
                    {
                        "expr": 'sum(rate(proxy_upstream_total{job="sarina-server"}[5m]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Global Upstream",
                "type": "stat",
            },
            {
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-purple", "value": None}],
                        },
                        "unit": "reqps",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 10, "y": 0},
                "id": 20,
                "options": {
                    "colorMode": "background",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "targets": [
                    {
                        "expr": 'sum(rate(proxy_requests_total{job="sarina-server"}[5m]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Global Requests",
                "type": "stat",
            },
            {
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-orange", "value": None}],
                        },
                        "unit": "decbytes",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 15, "y": 0},
                "id": 22,
                "options": {
                    "colorMode": "background",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "targets": [
                    {
                        "expr": 'sum(increase(proxy_downstream_total{job="sarina-server"}[24h])) + sum(increase(proxy_upstream_total{job="sarina-server"}[24h]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "Global Daily Traffic",
                "type": "stat",
            },
            {
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-green", "value": None}],
                        },
                        "unit": "Bps",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 0, "y": 4},
                "id": 4,
                "options": {
                    "colorMode": "none",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "repeat": "cluster",
                "repeatDirection": "v",
                "targets": [
                    {
                        "expr": 'sum(rate(proxy_downstream_total{job="sarina-server",cluster="$cluster"}[5m]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "$cluster - Downstream",
                "type": "stat",
            },
            {
                "datasource": "Prometheus",
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-blue", "value": None}],
                        },
                        "unit": "Bps",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 5, "y": 4},
                "id": 6,
                "options": {
                    "colorMode": "none",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "repeat": "cluster",
                "repeatDirection": "v",
                "targets": [
                    {
                        "expr": 'sum(rate(proxy_upstream_total{job="sarina-server",cluster="$cluster"}[5m]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "$cluster - Upstream",
                "type": "stat",
            },
            {
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-purple", "value": None}],
                        },
                        "unit": "reqps",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 10, "y": 4},
                "id": 8,
                "options": {
                    "colorMode": "none",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "repeat": "cluster",
                "repeatDirection": "v",
                "targets": [
                    {
                        "expr": 'sum(rate(proxy_requests_total{job="sarina-server",cluster="$cluster"}[5m]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "$cluster - Requests",
                "type": "stat",
            },
            {
                "datasource": "Prometheus",
                "description": "",
                "fieldConfig": {
                    "defaults": {
                        "color": {"mode": "thresholds"},
                        "mappings": [],
                        "thresholds": {
                            "mode": "absolute",
                            "steps": [{"color": "semi-dark-orange", "value": None}],
                        },
                        "unit": "decbytes",
                    },
                    "overrides": [],
                },
                "gridPos": {"h": 4, "w": 5, "x": 15, "y": 4},
                "id": 10,
                "options": {
                    "colorMode": "none",
                    "graphMode": "area",
                    "justifyMode": "auto",
                    "orientation": "auto",
                    "reduceOptions": {
                        "calcs": ["lastNotNull"],
                        "fields": "",
                        "values": False,
                    },
                    "textMode": "value",
                },
                "pluginVersion": "9.1.7",
                "repeat": "cluster",
                "repeatDirection": "v",
                "targets": [
                    {
                        "expr": 'sum(increase(proxy_downstream_total{job="sarina-server", cluster="$cluster"}[24h])) + sum(increase(proxy_upstream_total{job="sarina-server",cluster="$cluster"}[24h]))',
                        "legendFormat": "__auto",
                        "range": True,
                        "refId": "A",
                    }
                ],
                "title": "$cluster- Daily",
                "type": "stat",
            },
        ],
        "schemaVersion": 37,
        "style": "dark",
        "tags": [],
        "templating": {
            "list": [
                {
                    "current": {"selected": False, "text": "All", "value": "$__all"},
                    "datasource": "Prometheus",
                    "definition": "label_values(proxy_requests_total,cluster)",
                    "hide": 1,
                    "includeAll": True,
                    "label": "Cluster",
                    "multi": False,
                    "name": "cluster",
                    "options": [],
                    "query": {
                        "query": "label_values(proxy_requests_total,cluster)",
                        "refId": "StandardVariableQuery",
                    },
                    "refresh": 1,
                    "regex": "",
                    "skipUrlSync": False,
                    "sort": 1,
                    "type": "query",
                }
            ]
        },
        "time": {"from": "now-6h", "to": "now"},
        "timepicker": {},
        "timezone": "",
        "title": "Overview",
        "uid": "m5ZbtiS4k",
        "version": 8,
        "weekStart": "",
    },
    indent=4,
)
