explorer_url <- "https://ourworldindata.org/explorers/monkeypox?facet=none&hideControls=false&Metric=Confirmed+cases&Frequency=7-day+average&Shown+by=Date+of+confirmation&country=~OWID_WRL"
top <- df[location != "World" & !is.na(total_confirmed_by_confirmation), max(total_confirmed_by_confirmation, na.rm = T), location]
setorder(top, -V1)
update <- sprintf(
  "Monkeypox update:\n%s total confirmed cases\n+%s per day (rolling average)\n\nCountries with the most confirmed cases:\n%s\n\nData by @globaldothealth: %s",
  max(df$total_confirmed_by_confirmation, na.rm = T),
  round(latest_avg),
  paste0(sprintf("%s: %s", head(top$location, 5), head(top$V1, 5)), collapse = "\n"),
  explorer_url
)
clipr::write_clip(update)
browseURL(explorer_url)
browseURL("https://twitter.com/compose/tweet")
