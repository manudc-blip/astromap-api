import type { PlanetDetails, UiLanguage } from "../types/astromap";

type Props = {
  language: UiLanguage;
  availablePlanets: string[];
  selectedPlanet: string | null;
  details: PlanetDetails | null;
  onSelectPlanet: (planet: string) => void;
};

export function DetailsPanel({
  language,
  availablePlanets,
  selectedPlanet,
  details,
  onSelectPlanet,
}: Props) {
  const isEn = language === "en";

  const copyText = async () => {
    if (!details) return;

    const parts: string[] = [details.title];

    if (details.positionLines.length) {
      parts.push(`${isEn ? "Position" : "Position"}:\n${details.positionLines.join("\n")}`);
    }

    if (details.aspectLines.length) {
      parts.push(`${isEn ? "Aspects" : "Aspects"}:\n${details.aspectLines.join("\n")}`);
    }

    if (details.ephemerisLines.length) {
      parts.push(`${isEn ? "Ephemeris" : "Éphémérides"}:\n${details.ephemerisLines.join("\n")}`);
    }

    await navigator.clipboard.writeText(parts.join("\n\n"));
  };

  return (
    <aside className="gm-details-card">
      <div className="gm-details-header">
        <div className="gm-details-title">
          {isEn ? "Details" : "Détails"}
        </div>
        <button
          type="button"
          className="gm-copy-btn"
          disabled={!details}
          onClick={copyText}
        >
          {isEn ? "Copy" : "Copier"}
        </button>
      </div>

      <div className="gm-planet-picker">
        {availablePlanets.map((planet) => (
          <button
            key={planet}
            type="button"
            className={`gm-planet-chip ${selectedPlanet === planet ? "is-active" : ""}`}
            onClick={() => onSelectPlanet(planet)}
          >
            {planet}
          </button>
        ))}
      </div>

      {!details && (
        <div className="gm-details-empty">
          {isEn
            ? "Select a planet here. Direct click on the SVG will come in the next phase."
            : "Sélectionne une planète ici. Le clic direct sur le SVG viendra dans la phase suivante."}
        </div>
      )}

      {!!details && (
        <div className="gm-details-body">
          <div className="gm-details-planet" style={{ color: details.color }}>
            {details.title}
          </div>

          <div className="gm-details-section">
            <div className="gm-details-section-title">
              {isEn ? "Position" : "Position"}
            </div>
            {details.positionLines.length ? (
              details.positionLines.map((line) => (
                <div key={line} className="gm-details-line">{line}</div>
              ))
            ) : (
              <div className="gm-details-line gm-muted">—</div>
            )}
          </div>

          <div className="gm-details-section">
            <div className="gm-details-section-title">
              {isEn ? "Aspects" : "Aspects"}
            </div>
            {details.aspectLines.length ? (
              details.aspectLines.map((line) => (
                <div key={line} className="gm-details-line">{line}</div>
              ))
            ) : (
              <div className="gm-details-line gm-muted">—</div>
            )}
          </div>

          <div className="gm-details-section">
            <div className="gm-details-section-title">
              {isEn ? "Ephemeris" : "Éphémérides"}
            </div>
            {details.ephemerisLines.length ? (
              details.ephemerisLines.map((line) => (
                <div key={line} className="gm-details-line">{line}</div>
              ))
            ) : (
              <div className="gm-details-line gm-muted">—</div>
            )}
          </div>
        </div>
      )}
    </aside>
  );
}
