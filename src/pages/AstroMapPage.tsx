import { useEffect, useMemo, useState } from "react";
import { AstroSidebar } from "../components/AstroSidebar";
import { DetailsPanel } from "../components/DetailsPanel";
import { buildThemeRequestPayload, buildTransitsRequestPayload, createDefaultFormState } from "../lib/datetime";
import { getInterpretationHtml, getSvgForTab, getThemeJson, getTransitsJson, getTransitsSvg } from "../lib/api";
import { buildPlanetDetails, getPlanetNames } from "../lib/details";
import type { AstroFormState, ChartPayload, DetailOrigin, TabKey } from "../types/astromap";

const TABS: { key: TabKey; fr: string; en: string }[] = [
  { key: "ecliptic", fr: "Écliptique", en: "Ecliptic" },
  { key: "domitude", fr: "Domitude", en: "Domitude" },
  { key: "ret", fr: "RET / HP", en: "RET / HP" },
  { key: "transits", fr: "Transits", en: "Transits" },
  { key: "aspects", fr: "Aspects", en: "Aspects" },
  { key: "interpretation", fr: "Interprétation", en: "Interpretation" },
];

type CacheState = Partial<Record<TabKey, string>>;

function downloadTextFile(filename: string, content: string, mime: string) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
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
  const [selectedPlanet, setSelectedPlanet] = useState<string | null>(null);
  const [selectedOrigin, setSelectedOrigin] = useState<DetailOrigin>("natal");

  const isEn = form.language === "en";

  const updateField = <K extends keyof AstroFormState>(key: K, value: AstroFormState[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
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

    const svg = await getSvgForTab(tab as Exclude<TabKey, "interpretation" | "transits">, themeReq);
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
      setSelectedPlanet(null);
      setSelectedOrigin("natal");

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

  useEffect(() => {
    if (activeTab === "transits") {
      setSelectedOrigin("transits");
    } else {
      setSelectedOrigin("natal");
    }
    setSelectedPlanet(null);
  }, [activeTab]);

  const handleReset = () => {
    setForm(createDefaultFormState());
    setSubmittedForm(null);
    setThemePayload(null);
    setTransitsPayload(null);
    setCache({});
    setError(null);
    setCoordsLocked(false);
    setSelectedPlanet(null);
    setSelectedOrigin("natal");
    setActiveTab("ecliptic");
  };

  const handleExport = () => {
    const current = cache[activeTab];
    if (!current) return;

    if (activeTab === "interpretation") {
      downloadTextFile("astromap-interpretation.html", current, "text/html;charset=utf-8");
      return;
    }

    downloadTextFile(`astromap-${activeTab}.svg`, current, "image/svg+xml;charset=utf-8");
  };

  const currentContent = useMemo(() => cache[activeTab] || "", [cache, activeTab]);

  const detailsPayload = selectedOrigin === "transits" ? transitsPayload : themePayload;
  const availablePlanets = useMemo(() => getPlanetNames(detailsPayload), [detailsPayload]);
  const detailState = useMemo(
    () => buildPlanetDetails(detailsPayload, selectedPlanet, form.language, selectedOrigin),
    [detailsPayload, selectedPlanet, form.language, selectedOrigin]
  );

  const showDetails = activeTab === "ecliptic" || activeTab === "domitude" || activeTab === "transits";

  return (
    <div className="gm-app">
      <AstroSidebar
        form={form}
        activeTab={activeTab}
        loading={loading}
        coordsLocked={coordsLocked}
        onChange={updateField}
        onReset={handleReset}
        onCalculate={handleCalculate}
        onExport={handleExport}
        onCitySelected={() => setCoordsLocked(true)}
        onCoordsManualEdit={() => setCoordsLocked(false)}
      />

      <main className="gm-main">
        <div className="gm-tabs">
          {TABS.map((tab) => (
            <button
              key={tab.key}
              type="button"
              className={`gm-tab ${activeTab === tab.key ? "is-active" : ""}`}
              onClick={() => setActiveTab(tab.key)}
            >
              {isEn ? tab.en : tab.fr}
            </button>
          ))}
        </div>

        <div className={`gm-main-grid ${showDetails ? "has-details" : ""}`}>
          {showDetails && (
            <DetailsPanel
              language={form.language}
              availablePlanets={availablePlanets}
              selectedPlanet={selectedPlanet}
              details={detailState}
              onSelectPlanet={setSelectedPlanet}
            />
          )}

          <div className="gm-result-wrap">
            {error && <div className="gm-error">{error}</div>}

            {!submittedForm && !error && (
              <div className="gm-empty">
                {isEn
                  ? "Fill the sidebar and click Compute."
                  : "Renseigne la sidebar puis clique sur Calculer."}
              </div>
            )}

            {!!submittedForm && !error && activeTab !== "interpretation" && !!currentContent && (
              <div
                className="gm-svg-panel"
                dangerouslySetInnerHTML={{ __html: currentContent }}
              />
            )}

            {!!submittedForm && !error && activeTab === "interpretation" && !!currentContent && (
              <iframe
                title="interpretation"
                className="gm-interpretation-frame"
                srcDoc={currentContent}
              />
            )}
          </div>
        </div>

        <div className="gm-footer">
          {themePayload ? (
            <span>{isEn ? "Backend connected" : "Backend connecté"}</span>
          ) : (
            <span>{isEn ? "No calculated chart yet" : "Aucun thème calculé pour l’instant"}</span>
          )}
        </div>
      </main>
    </div>
  );
}
