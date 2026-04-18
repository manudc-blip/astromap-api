import { useEffect, useMemo, useState } from "react";
import AstroSidebar from "../components/AstroSidebar";
import {
  buildThemeRequestPayload,
  buildTransitsRequestPayload,
  createDefaultFormState,
} from "../lib/datetime";
import {
  getInterpretationHtml,
  getSvgForTab,
  getThemeJson,
  getTransitsJson,
  getTransitsSvg,
} from "../lib/api";
import type { AstroFormState, ChartPayload, TabKey } from "../types/astromap";

const TABS: { key: TabKey; fr: string; en: string }[] = [
  { key: "ecliptic", fr: "Écliptique", en: "Ecliptic" },
  { key: "domitude", fr: "Domitude", en: "Domitude" },
  { key: "ret", fr: "RET / HP", en: "RET / HP" },
  { key: "transits", fr: "Transits", en: "Transits" },
  { key: "aspects", fr: "Aspects", en: "Aspects" },
  { key: "interpretation", fr: "Interprétation", en: "Interpretation" },
];

type CacheState = Partial<Record<TabKey, string>>;
type TimeRef = "HO" | "TU";
type CoordsDisplayMode = "DEC" | "DMS";
type IdentMode = "ID" | "WORLD";

function downloadTextFile(filename: string, content: string, mime: string) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function pad2(value: number) {
  return String(value).padStart(2, "0");
}

function pad4(value: number) {
  return String(value).padStart(4, "0");
}

function buildSafeNatalDate(form: any) {
  const year = Number(form.year || 2000);
  const month = Math.max(1, Number(form.month || 1));
  const day = Math.max(1, Number(form.day || 1));
  const hour = Math.max(0, Number(form.hour || 0));
  const minute = Math.max(0, Number(form.minute || 0));

  return new Date(year, month - 1, day, hour, minute, 0, 0);
}

function buildSafeTransitDate(form: any) {
  const year = Number(form.transitYear || 2000);
  const month = Math.max(1, Number(form.transitMonth || 1));
  const day = Math.max(1, Number(form.transitDay || 1));

  return new Date(year, month - 1, day, 12, 0, 0, 0);
}

export default function AstroMapPage() {
  const [form, setForm] = useState<AstroFormState>(createDefaultFormState());
  const [submittedForm, setSubmittedForm] = useState<AstroFormState | null>(null);
  const [activeTab, setActiveTab] = useState<TabKey>("ecliptic");
  const [cache, setCache] = useState<CacheState>({});
  const [themePayload, setThemePayload] = useState<ChartPayload | null>(null);
  const [transitsPayload, setTransitsPayload] = useState<ChartPayload | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [coordsLocked, setCoordsLocked] = useState(false);
  const [coordsDisplayMode, setCoordsDisplayMode] =
    useState<CoordsDisplayMode>("DEC");
  const [identMode, setIdentMode] = useState<IdentMode>("ID");
  const [transitPanelExpanded, setTransitPanelExpanded] = useState(true);

  const formAny = form as any;
  const isEn = (formAny.language ?? "fr") === "en";

  const getTimeRef = (state: any): TimeRef => {
    return (state.timeRef ?? state.timeReference ?? "HO") as TimeRef;
  };

  const getTransitAspectMode = (state: any): "TN" | "TT" => {
    return (state.transitAspectMode ?? "TN") as "TN" | "TT";
  };

  const setFormPatch = (patch: Record<string, any>) => {
    setForm((prev) => ({ ...(prev as any), ...patch }));
  };

  const handleSidebarFormChange = (patch: Record<string, any>) => {
    const normalized = { ...patch } as Record<string, any>;

    if ("lang" in normalized) {
      normalized.language = normalized.lang;
      delete normalized.lang;
    }

    setForm((prev) => ({ ...(prev as any), ...normalized }));

    if ("lat" in normalized || "lon" in normalized) {
      setCoordsLocked(false);
    }
  };

  const shiftNatalDate = (step: 1 | -1) => {
    const dt = buildSafeNatalDate(formAny);
    dt.setDate(dt.getDate() + step);

    setFormPatch({
      day: pad2(dt.getDate()),
      month: pad2(dt.getMonth() + 1),
      year: pad4(dt.getFullYear()),
    });
  };

  const shiftNatalTime = (step: 1 | -1) => {
    const dt = buildSafeNatalDate(formAny);
    dt.setHours(dt.getHours() + step);

    setFormPatch({
      day: pad2(dt.getDate()),
      month: pad2(dt.getMonth() + 1),
      year: pad4(dt.getFullYear()),
      hour: pad2(dt.getHours()),
      minute: pad2(dt.getMinutes()),
    });
  };

  const shiftTransitDate = (step: 1 | -1) => {
    const dt = buildSafeTransitDate(formAny);
    dt.setDate(dt.getDate() + step);

    setFormPatch({
      transitDay: pad2(dt.getDate()),
      transitMonth: pad2(dt.getMonth() + 1),
      transitYear: pad4(dt.getFullYear()),
    });
  };

  const toggleTimeRef = () => {
    const current = getTimeRef(formAny);
    const next: TimeRef = current === "HO" ? "TU" : "HO";

    if ("timeRef" in formAny || !("timeReference" in formAny)) {
      setFormPatch({ timeRef: next });
    } else {
      setFormPatch({ timeReference: next });
    }
  };

  const toggleCoordsDisplay = () => {
    setCoordsDisplayMode((prev) => (prev === "DEC" ? "DMS" : "DEC"));
  };

  const toggleTransitPanel = () => {
    setTransitPanelExpanded((prev) => !prev);
  };

  const loadTab = async (tab: TabKey, currentForm: AstroFormState, force = false) => {
    if (!force && cache[tab]) return;

    const themeReq = buildThemeRequestPayload(currentForm);

    if (tab === "interpretation") {
      const html = await getInterpretationHtml(themeReq);
      setCache((prev) => ({ ...prev, interpretation: html }));
      return;
    }

    if (tab === "transits") {
      const transitReq = buildTransitsRequestPayload(currentForm);
      const [svg, json] = await Promise.all([
        getTransitsSvg(transitReq),
        getTransitsJson(transitReq),
      ]);

      setTransitsPayload(json.data as ChartPayload);
      setCache((prev) => ({ ...prev, transits: svg }));
      return;
    }

    const svg = await getSvgForTab(
      tab as Exclude<TabKey, "interpretation" | "transits">,
      themeReq
    );

    setCache((prev) => ({ ...prev, [tab]: svg }));
  };

  const handleCalculate = async () => {
    setError(null);
    setLoading(true);

    try {
      const nextSubmitted = { ...form };
      const themeReq = buildThemeRequestPayload(nextSubmitted);
      const themeData = await getThemeJson(themeReq);

      setSubmittedForm(nextSubmitted);
      setThemePayload(themeData.data as ChartPayload);
      setTransitsPayload(null);
      setCache({});

      await loadTab(activeTab, nextSubmitted, true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!submittedForm) return;

    let cancelled = false;

    (async () => {
      try {
        setLoading(true);
        await loadTab(activeTab, submittedForm);
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Erreur inconnue");
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [activeTab, submittedForm]);

  const handleReset = () => {
    setForm(createDefaultFormState());
    setSubmittedForm(null);
    setThemePayload(null);
    setTransitsPayload(null);
    setCache({});
    setError(null);
    setCoordsLocked(false);
    setCoordsDisplayMode("DEC");
    setIdentMode("ID");
    setTransitPanelExpanded(true);
    setActiveTab("ecliptic");
  };

  const handleExport = () => {
    const current = cache[activeTab];
    if (!current) return;

    if (activeTab === "interpretation") {
      downloadTextFile(
        "astromap-interpretation.html",
        current,
        "text/html;charset=utf-8"
      );
      return;
    }

    downloadTextFile(
      `astromap-${activeTab}.svg`,
      current,
      "image/svg+xml;charset=utf-8"
    );
  };

  const currentContent = useMemo(() => cache[activeTab] || "", [cache, activeTab]);

  const sidebarForm = {
    name: formAny.name ?? "",
    day: formAny.day ?? "",
    month: formAny.month ?? "",
    year: formAny.year ?? "",
    hour: formAny.hour ?? "",
    minute: formAny.minute ?? "",
    timeRef: getTimeRef(formAny),

    city: formAny.city ?? "",
    lat: formAny.lat ?? "",
    lon: formAny.lon ?? "",
    timezone: formAny.timezone ?? formAny.tz ?? "Europe/Paris",

    lang: (formAny.language ?? "fr") as "fr" | "en",

    transitDay: formAny.transitDay ?? "",
    transitMonth: formAny.transitMonth ?? "",
    transitYear: formAny.transitYear ?? "",
    transitAspectMode: getTransitAspectMode(formAny),
    transitPanelExpanded,
  };

  return (
    <div className="astromap-app">
      <aside className="astromap-sidebar-shell">
        <AstroSidebar
          form={sidebarForm}
          activeTab={activeTab}
          identMode={identMode}
          dnSource=""
          cityHint={isEn ? "Assisted entry" : "Saisie assistée"}
          coordsLocked={coordsLocked}
          coordsDisplayMode={coordsDisplayMode}
          showDnSuggestions={false}
          dnSuggestions={[]}
          showCitySuggestions={false}
          citySuggestions={[]}
          onFormChange={handleSidebarFormChange}
          onToggleIdentMode={() =>
            setIdentMode((prev) => (prev === "ID" ? "WORLD" : "ID"))
          }
          onToggleTimeRef={toggleTimeRef}
          onToggleCoordsDisplay={toggleCoordsDisplay}
          onToggleTransitPanel={toggleTransitPanel}
          onShiftNatalDate={shiftNatalDate}
          onShiftNatalTime={shiftNatalTime}
          onShiftTransitDate={shiftTransitDate}
          onCompute={handleCalculate}
          onReset={handleReset}
          onExport={handleExport}
        />
      </aside>

      <main className="astromap-main">
        <div className="astromap-tabs">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              type="button"
              className={`astromap-tab ${activeTab === tab.key ? "astromap-tab--active" : ""}`}
              onClick={() => setActiveTab(tab.key)}
            >
              {isEn ? tab.en : tab.fr}
            </button>
          ))}
        </div>

        <div className="astromap-stage">
          {error ? <div className="gm-error">{error}</div> : null}

          {!submittedForm && !error ? (
            <div className="gm-empty">
              {isEn
                ? "Fill the sidebar and click Compute."
                : "Renseigne la sidebar puis clique sur Calculer."}
            </div>
          ) : null}

          {!!submittedForm && !error && activeTab !== "interpretation" && !!currentContent ? (
            <div className="astromap-canvas-host">
              <div
                className="gm-svg-panel"
                dangerouslySetInnerHTML={{ __html: currentContent }}
              />
            </div>
          ) : null}

          {!!submittedForm && !error && activeTab === "interpretation" && !!currentContent ? (
            <iframe
              title="interpretation"
              className="gm-interpretation-frame"
              srcDoc={currentContent}
            />
          ) : null}
        </div>

        <div className="gm-footer">
          {loading ? (
            <span>{isEn ? "Loading..." : "Chargement..."}</span>
          ) : themePayload ? (
            <span>{isEn ? "Backend connected" : "Backend connecté"}</span>
          ) : (
            <span>
              {isEn
                ? "No calculated chart yet"
                : "Aucun thème calculé pour l’instant"}
            </span>
          )}
        </div>
      </main>
    </div>
  );
}
