export type TabKey =
  | "ecliptic"
  | "domitude"
  | "ret"
  | "transits"
  | "aspects"
  | "interpretation";

export type TimeReference = "HO" | "TU";
export type TransitAspectMode = "TN" | "TT";
export type UiLanguage = "fr" | "en";

export interface AstroFormState {
  name: string;

  day: string;
  month: string;
  year: string;

  hour: string;
  minute: string;
  timeRef: TimeReference;

  cityQuery: string;
  latitude: string;
  longitude: string;
  tz: string;

  language: UiLanguage;

  transitDay: string;
  transitMonth: string;
  transitYear: string;
  transitAspectMode: TransitAspectMode;
}

export interface ThemeSettingsPayload {
  house_system: string;
  language: UiLanguage;
}

export interface ThemeRequestPayload {
  name: string;
  datetime_local: string;
  latitude: number;
  longitude: number;
  tz: string;
  settings: ThemeSettingsPayload;
}

export interface TransitsRequestPayload extends ThemeRequestPayload {
  transit_datetime_local: string;
  aspect_mode: TransitAspectMode;
}

export interface ThemeResponsePayload {
  data: Record<string, unknown>;
}

export interface CitySearchItem {
  display: string;
  name: string;
  lat: number;
  lon: number;
  tz: string;
}
