import type { AstroFormState, CitySearchItem, TabKey } from "../types/astromap";
import { CityAutocomplete } from "./CityAutocomplete";

type Props = {
  form: AstroFormState;
  activeTab: TabKey;
  loading: boolean;
  coordsLocked: boolean;
  onChange: <K extends keyof AstroFormState>(key: K, value: AstroFormState[K]) => void;
  onReset: () => void;
  onCalculate: () => void;
  onExport: () => void;
  onCitySelected: () => void;
  onCoordsManualEdit: () => void;
};

export function AstroSidebar({
  form,
  activeTab,
  loading,
  coordsLocked,
  onChange,
  onReset,
  onCalculate,
  onExport,
  onCitySelected,
  onCoordsManualEdit,
}: Props) {
  const isEn = form.language === "en";

  const ui = isEn
    ? {
        identification: "Identification",
        name: "Name (optional)",
        dateTime: "Date & time",
        date: "Date",
        time: "Time",
        timeRef: "Time reference",
        city: "City (search)",
        cityHint: "Assisted input",
        location: "Location",
        latLon: "Latitude, Longitude",
        tz: "Time zone",
        language: "Language",
        options: "Options",
        actions: "Actions",
        reset: "Reset",
        calculate: "Compute",
        export: "Export",
        transitDate: "Transit date",
        aspectMode: "Aspect mode",
        tn: "Transit → Natal",
        tt: "Between transits",
      }
    : {
        identification: "Identification",
        name: "Nom (facultatif)",
        dateTime: "Date & heure",
        date: "Date",
        time: "Heure",
        timeRef: "Référence heure",
        city: "Ville (recherche)",
        cityHint: "Saisie assistée",
        location: "Localisation",
        latLon: "Latitude, Longitude",
        tz: "Fuseau horaire",
        language: "Langue",
        options: "Options",
        actions: "Actions",
        reset: "Réinitialiser",
        calculate: "Calculer",
        export: "Exporter",
        transitDate: "Date du transit",
        aspectMode: "Mode des aspects",
        tn: "Transits → Natal",
        tt: "Entre transits",
      };

  const handleCitySelect = (city: CitySearchItem) => {
    onChange("cityQuery", city.display);
    onChange("latitude", String(city.lat));
    onChange("longitude", String(city.lon));
    onChange("tz", city.tz);
    onCitySelected();
  };

  return (
    <aside className="gm-sidebar">
      <div className="gm-logo-block">
        <div className="gm-logo-title">GéoAstro</div>
        <div className="gm-logo-subtitle">Module AstroMap</div>
      </div>

      <section className="gm-section">
        <h3>{ui.identification}</h3>
        <label>{ui.name}</label>
        <input
          className="gm-input"
          value={form.name}
          onChange={(e) => onChange("name", e.target.value)}
        />
      </section>

      <section className="gm-section">
        <h3>{ui.dateTime}</h3>

        <label>{ui.date}</label>
        <div className="gm-inline-3">
          <input className="gm-input" value={form.day} onChange={(e) => onChange("day", e.target.value)} />
          <input className="gm-input" value={form.month} onChange={(e) => onChange("month", e.target.value)} />
          <input className="gm-input" value={form.year} onChange={(e) => onChange("year", e.target.value)} />
        </div>

        <label>{ui.time}</label>
        <div className="gm-inline-2">
          <input className="gm-input" value={form.hour} onChange={(e) => onChange("hour", e.target.value)} />
          <input className="gm-input" value={form.minute} onChange={(e) => onChange("minute", e.target.value)} />
        </div>

        <label>{ui.timeRef}</label>
        <div className="gm-radio-row">
          <label><input type="radio" checked={form.timeRef === "HO"} onChange={() => onChange("timeRef", "HO")} /> HO</label>
          <label><input type="radio" checked={form.timeRef === "TU"} onChange={() => onChange("timeRef", "TU")} /> TU</label>
        </div>
      </section>

      <section className="gm-section">
        <h3>{ui.location}</h3>

        <label>{ui.city}</label>
        <CityAutocomplete
          value={form.cityQuery}
          language={form.language}
          onChange={(value) => {
            onChange("cityQuery", value);
          }}
          onSelect={handleCitySelect}
        />
        <div className="gm-hint">{ui.cityHint}</div>

        <label>{ui.latLon}</label>
        <div className="gm-inline-2">
          <input
            className="gm-input"
            value={form.latitude}
            readOnly={coordsLocked}
            onChange={(e) => {
              onCoordsManualEdit();
              onChange("latitude", e.target.value);
            }}
          />
          <input
            className="gm-input"
            value={form.longitude}
            readOnly={coordsLocked}
            onChange={(e) => {
              onCoordsManualEdit();
              onChange("longitude", e.target.value);
            }}
          />
        </div>

        <label>{ui.tz}</label>
        <input
          className="gm-input"
          value={form.tz}
          onChange={(e) => onChange("tz", e.target.value)}
        />
      </section>

      <section className="gm-section">
        <h3>{ui.options}</h3>

        <label>{ui.language}</label>
        <div className="gm-radio-row">
          <label><input type="radio" checked={form.language === "fr"} onChange={() => onChange("language", "fr")} /> FR</label>
          <label><input type="radio" checked={form.language === "en"} onChange={() => onChange("language", "en")} /> EN</label>
        </div>

        {activeTab === "transits" && (
          <>
            <div className="gm-divider" />

            <label>{ui.transitDate}</label>
            <div className="gm-inline-3">
              <input className="gm-input" value={form.transitDay} onChange={(e) => onChange("transitDay", e.target.value)} />
              <input className="gm-input" value={form.transitMonth} onChange={(e) => onChange("transitMonth", e.target.value)} />
              <input className="gm-input" value={form.transitYear} onChange={(e) => onChange("transitYear", e.target.value)} />
            </div>

            <label>{ui.aspectMode}</label>
            <div className="gm-radio-col">
              <label>
                <input
                  type="radio"
                  checked={form.transitAspectMode === "TN"}
                  onChange={() => onChange("transitAspectMode", "TN")}
                />
                {ui.tn}
              </label>
              <label>
                <input
                  type="radio"
                  checked={form.transitAspectMode === "TT"}
                  onChange={() => onChange("transitAspectMode", "TT")}
                />
                {ui.tt}
              </label>
            </div>
          </>
        )}
      </section>

      <section className="gm-section">
        <h3>{ui.actions}</h3>
        <div className="gm-actions">
          <button type="button" className="gm-btn" onClick={onReset} disabled={loading}>
            {ui.reset}
          </button>
          <button type="button" className="gm-btn gm-btn-primary" onClick={onCalculate} disabled={loading}>
            {loading ? "..." : ui.calculate}
          </button>
          <button type="button" className="gm-btn" onClick={onExport}>
            {ui.export}
          </button>
        </div>
      </section>
    </aside>
  );
}
