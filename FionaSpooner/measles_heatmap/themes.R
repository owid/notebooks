# Import fonts
font_import(pattern = c("Lato", "Playfair Display"), prompt=FALSE)
loadfonts(device = "all") # use "win" for Windows, "mac" for macOS

# Add OWID discrete colour palette
owid_discrete_palette <- c(
  "Purple" = "#6D3E91",
  "Dark Orange" = "#C05917",
  "Light Teal" = "#58AC8C",
  "Blue" = "#286BBB",
  "Maroon" = "#883039",
  "Camel" = "#BC8E5A",
  "Midnight Blue" = "#00295B",
  "Dusty Coral" = "#C15065",
  "Dark Olive Green" = "#18470F",
  "Dark Copper" = "#9A5129",
  "Peach" = "#E56E5A",
  "Mauve" = "#A2559C",
  "Turquoise" = "#38AABA",
  "Olive Green" = "#578145",
  "Cherry" = "#970046",
  "Teal" = "#00847E",
  "Rusty Orange" = "#B13507",
  "Denim" = "#4C6A9C",
  "Fuchsia" = "#CF0A66",
  "Tealish Green" = "#00875E",
  "Copper" = "#B16214",
  "Dark Mauve" = "#8C4569",
  "Lime" = "#3B8E1D",
  "Coral" = "#D73C50"
)
# Define OWID theme function

theme_owid_combined <- function(base_size = 12, base_family = "Lato") {
  
  list(
    theme_minimal() %+replace%    # Replace elements we want to change
      
      theme(
        
        # background elements
        panel.background = element_rect( # Facet background
          fill = "white", 
          color = NA), 
        
        plot.background = element_rect( # Plot background
          fill = "white", 
          color = NA),  
        
        panel.border = element_rect( # Facet border
          color = "grey50", 
          size = 0.5, 
          fill = NA), 
        
        plot.margin = margin( # Plot margins
          t = 10, 
          r = 20, 
          b = 20, 
          l = 10),
        
        plot.caption.position = "plot", # Plot caption left-aligned with plot
        
        legend.position = "top",  # Legend at top
        
        # grid elements
        
        panel.grid.major = element_blank(),    # Remove major gridlines
        
        panel.grid.minor = element_blank(),    # Remove minor gridlines
        
        axis.ticks = element_line(color = "grey70"), # Axis ticks light grey
        
        axis.ticks.length = unit(4, "pt"), # Axis ticks 4 pt length
        
        # legend elements
        legend.key.width = unit(2, "cm"),    # Adjust legend key width
        
        legend.text = element_text(
          size = 10, 
          family = "Lato"),                  
        
        legend.spacing.x = unit(0.5, "cm"),  # Add spacing between legend items
        
        # text elements
        text = element_text(  # Make most text Lato and grey
          family = "Lato", 
          color = "grey50"),
        
        plot.title = element_text( # Plot title
          family = "Playfair Display SemiBold", 
          color = "grey10",
          size = 25,
          face = "bold", 
          hjust = 0,                # left align
          vjust = 2),
        
        plot.subtitle = element_text( # Subtitle
          size = 15, 
          hjust = 0,                # left align
          color = "grey30",
          vjust = 1.5),
        
        axis.text = element_text( # Axis labels
          size = 10, 
          angle = 0, 
          hjust = 0.5, 
          color = "grey50"),
        
        axis.title = element_text( # Axis titles
          size = 12, 
          color = "grey50"),
        
        axis.title.y = element_blank(),
        
        plot.caption = element_text( # Caption
          size = 10, 
          color = "grey50",
          hjust = 0,
          vjust = -2),
        
        strip.text = element_text( # Facet titles
          size = 12, 
          face = "bold", 
          color = "grey30", 
          hjust = 0)),  # left align
    
    #scale_fill_manual(values = owid_discrete_palette),
    scale_color_manual(values = owid_discrete_palette)
  )
  
}


# Load the OWID logo from URL
logo_url <- "https://ourworldindata.org/uploads/2019/02/OurWorldinData-logo.png"
owid_logo <- magick::image_read(logo_url)

# Define plot dimensions for different aspect ratios
plot_dimensions <- list(
  vertical = list(width = 8, height = 10),    # Vertical plot dimensions
  horizontal = list(width = 10, height = 6), # Horizontal plot dimensions
  square = list(width = 8, height = 8)       # Square plot dimensions
)

# Helper function to fetch dimensions with named output for clarity
get_plot_dimensions <- function(aspect) {
  dims <- plot_dimensions[[aspect]]
  list(width = dims$width, height = dims$height)
}