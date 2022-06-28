latest_avg <- df[location == "World", tail(`7day_confirmed_by_confirmation`, 1)]
max_avg <- df[location == "World", max(`7day_confirmed_by_confirmation`, na.rm = T)]

if (latest_avg == max_avg) {
  
  explorer_url <- "https://ourworldindata.org/explorers/monkeypox?facet=none&hideControls=false&Metric=Confirmed+cases&Frequency=7-day+average&Shown+by=Date+of+confirmation&country=~OWID_WRL"
  
  top <- df[location != "World" & !is.na(total_confirmed_by_confirmation), max(total_confirmed_by_confirmation, na.rm = T), location]
  setorder(top, -V1)
  update <- sprintf(
    "Monkeypox: %s total confirmed cases in %s countries\n+%s per day (7-day average)\n\nData by @globaldothealth: %s",
    max(df$total_confirmed_by_confirmation, na.rm = T),
    df[total_confirmed_by_confirmation > 0, length(unique(location))],
    round(latest_avg),
    explorer_url
  )
  
  clipr::write_clip(update)
  browseURL(explorer_url)
  browseURL("https://twitter.com/compose/tweet")
  
}
