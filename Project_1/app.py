from __future__ import annotations

from html import escape
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from Calc_traffic import (
    DEFAULT_WORK_DAYS_PER_YEAR,
    CongestionInput,
    CongestionResult,
    calculate_congestion_impact,
)


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = BASE_DIR / "templates" / "index.html"
STYLES_PATH = BASE_DIR / "static" / "styles.css"
DEMO_VALUES = {
    "hourly_wage": "500",
    "normal_commute_mins": "35",
    "actual_commute_mins": "80",
    "work_days_per_year": str(DEFAULT_WORK_DAYS_PER_YEAR),
}


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _safe_value(values: dict[str, str], key: str, default: str) -> str:
    return escape(values.get(key, default))


def _safe_float(values: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(values.get(key, default))
    except (TypeError, ValueError):
        return default


def _build_graph_markup(result: CongestionResult, values: dict[str, str]) -> str:
    normal_commute = _safe_float(values, "normal_commute_mins")
    actual_commute = _safe_float(values, "actual_commute_mins")
    commute_scale = max(actual_commute, normal_commute, 1.0)
    benchmark_scale = max(result.annual_lost_hours, 168.0, 1.0)
    ideal_width = (normal_commute / commute_scale) * 100
    actual_width = (actual_commute / commute_scale) * 100
    benchmark_width = (168.0 / benchmark_scale) * 100
    user_width = (result.annual_lost_hours / benchmark_scale) * 100

    return f"""
    <section class=\"graph-panel\">
        <div class=\"graph-card\">
            <div class=\"graph-copy\">
                <span class=\"graph-kicker\">Commute comparison</span>
                <h3>Ideal vs rush-hour travel</h3>
            </div>
            <div class=\"bar-chart\" aria-label=\"Commute time comparison\">
                <div class=\"bar-row\">
                    <span class=\"bar-label\">Ideal one-way</span>
                    <div class=\"bar-track\"><span class=\"bar-fill ideal\" style=\"width: {ideal_width:.1f}%\"></span></div>
                    <strong class=\"bar-value\">{normal_commute:.1f} min</strong>
                </div>
                <div class=\"bar-row\">
                    <span class=\"bar-label\">Rush-hour one-way</span>
                    <div class=\"bar-track\"><span class=\"bar-fill actual\" style=\"width: {actual_width:.1f}%\"></span></div>
                    <strong class=\"bar-value\">{actual_commute:.1f} min</strong>
                </div>
            </div>
        </div>

        <div class=\"graph-card\">
            <div class=\"graph-copy\">
                <span class=\"graph-kicker\">Annual loss benchmark</span>
                <h3>Your delay vs Bengaluru average</h3>
            </div>
            <div class=\"bar-chart\" aria-label=\"Annual loss vs benchmark\">
                <div class=\"bar-row\">
                    <span class=\"bar-label\">City benchmark</span>
                    <div class=\"bar-track\"><span class=\"bar-fill benchmark\" style=\"width: {benchmark_width:.1f}%\"></span></div>
                    <strong class=\"bar-value\">168 hrs</strong>
                </div>
                <div class=\"bar-row\">
                    <span class=\"bar-label\">Your annual loss</span>
                    <div class=\"bar-track\"><span class=\"bar-fill user\" style=\"width: {user_width:.1f}%\"></span></div>
                    <strong class=\"bar-value\">{result.annual_lost_hours:.1f} hrs</strong>
                </div>
            </div>
        </div>
    </section>
    """


def _build_result_markup(result: CongestionResult, values: dict[str, str]) -> str:
    alert_markup = ""
    if result.exceeds_city_average:
        alert_markup = (
            '<p class="alert">Your annual time loss is above the Bengaluru benchmark '
            'of 168 hours.</p>'
        )

    graph_markup = _build_graph_markup(result, values)

    return f"""
    <section class=\"result-panel\">
        <div class=\"metric-grid\">
            <article class=\"metric-card\">
                <span class=\"metric-label\">Annual Time Lost</span>
                <strong class=\"metric-value\">{result.annual_lost_hours:.1f} hours</strong>
            </article>
            <article class=\"metric-card\">
                <span class=\"metric-label\">Equivalent Days</span>
                <strong class=\"metric-value\">{result.annual_lost_days:.1f} days</strong>
            </article>
            <article class=\"metric-card\">
                <span class=\"metric-label\">Lost Productivity</span>
                <strong class=\"metric-value\">Rs. {result.annual_financial_loss:,.2f}</strong>
            </article>
        </div>
        <p class=\"supporting-copy\">Daily delay impact: {result.daily_lost_hours:.2f} hours.</p>
        {graph_markup}
        {alert_markup}
    </section>
    """


def render_page(
    values: dict[str, str] | None = None,
    result: CongestionResult | None = None,
    error_message: str = "",
) -> bytes:
    values = values or {}
    template = _read_text(TEMPLATE_PATH)
    replacements = {
        "__HOURLY_WAGE__": _safe_value(values, "hourly_wage", ""),
        "__NORMAL_COMMUTE__": _safe_value(values, "normal_commute_mins", ""),
        "__ACTUAL_COMMUTE__": _safe_value(values, "actual_commute_mins", ""),
        "__WORK_DAYS__": _safe_value(
            values,
            "work_days_per_year",
            str(DEFAULT_WORK_DAYS_PER_YEAR),
        ),
        "__ERROR__": (
            f'<p class="error-banner">{escape(error_message)}</p>' if error_message else ""
        ),
        "__RESULT__": _build_result_markup(result, values) if result else "",
    }

    for placeholder, replacement in replacements.items():
        template = template.replace(placeholder, replacement)

    return template.encode("utf-8")


class CongestionTaxHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path in {"/", "/index.html"}:
            demo_input = CongestionInput(
                hourly_wage=float(DEMO_VALUES["hourly_wage"]),
                normal_commute_mins=float(DEMO_VALUES["normal_commute_mins"]),
                actual_commute_mins=float(DEMO_VALUES["actual_commute_mins"]),
                work_days_per_year=int(DEMO_VALUES["work_days_per_year"]),
            )
            self._send_html(
                render_page(
                    values=DEMO_VALUES,
                    result=calculate_congestion_impact(demo_input),
                )
            )
            return

        if self.path == "/static/styles.css":
            self._send_css(_read_text(STYLES_PATH).encode("utf-8"))
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Page not found")

    def do_POST(self) -> None:
        if self.path != "/calculate":
            self.send_error(HTTPStatus.NOT_FOUND, "Page not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")
        parsed = parse_qs(body)
        values = {key: value[0].strip() for key, value in parsed.items()}

        try:
            user_input = CongestionInput(
                hourly_wage=float(values.get("hourly_wage", "0")),
                normal_commute_mins=float(values.get("normal_commute_mins", "0")),
                actual_commute_mins=float(values.get("actual_commute_mins", "0")),
                work_days_per_year=int(
                    float(values.get("work_days_per_year", DEFAULT_WORK_DAYS_PER_YEAR))
                ),
            )
            result = calculate_congestion_impact(user_input)
            self._send_html(render_page(values=values, result=result))
        except ValueError as exc:
            self._send_html(render_page(values=values, error_message=str(exc)))

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, payload: bytes) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_css(self, payload: bytes) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/css; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    with ThreadingHTTPServer((host, port), CongestionTaxHandler) as server:
        print(f"Serving Personal Congestion Tax Calculator on http://{host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    run_server()