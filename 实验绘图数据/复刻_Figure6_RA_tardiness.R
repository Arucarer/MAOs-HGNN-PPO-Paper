# 使用 base R 复刻论文 Figure 6 的布局与视觉风格。
# 原论文未公开 100 次仿真的逐次数据，因此箱线图数据依据原图分布近似生成；
# 饼图中的胜率数字按照原图录入。

options(encoding = "UTF-8")

args <- commandArgs(trailingOnly = FALSE)
script_arg <- grep("^--file=", args, value = TRUE)
script_path <- normalizePath(sub("^--file=", "", script_arg[1]), winslash = "/")
project_root <- normalizePath(file.path(dirname(script_path), "..", ".."), winslash = "/")
output_dir <- file.path(project_root, "02_论文图片", "03_反应式学习调度")
output_stem <- file.path(output_dir, "复刻_Figure6_RA_tardiness")

dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

font_family <- "sans"
panel_background <- "#DDF5F4"
grid_color <- "#BFD0D0"
mean_color <- "#00952D"

method_colors <- c(
  EA = "#11998E",
  CT = "#FF7200",
  ET = "#C8B800",
  TT = "#E50078",
  UT = "#43B3E6",
  SQ = "#A6A6A6",
  `DRL-RA` = "#1400B5"
)

# 使用确定性分位点生成与原图箱体位置、离散程度相近的数据。
make_series <- function(center, spread, lower, upper, outliers = numeric()) {
  core_size <- 100 - length(outliers)
  probabilities <- seq(0.01, 0.99, length.out = core_size)
  values <- qnorm(probabilities, mean = center, sd = spread)
  values <- pmin(pmax(values, lower), upper)
  c(values, outliers)
}

scenario_data <- list(
  HH = list(
    CT = make_series(72, 5.5, 58, 84, c(33, 44, 49)),
    ET = make_series(48, 16.0, -10, 79),
    TT = make_series(-3, 14.0, -38, 48),
    UT = make_series(-28, 8.0, -50, -5),
    SQ = make_series(-12, 14.0, -42, 33),
    `DRL-RA` = make_series(80, 6.0, 61, 94, c(50, 52))
  ),
  HL = list(
    CT = make_series(74, 5.5, 60, 84, c(30, 46)),
    ET = make_series(47, 17.0, -15, 83),
    TT = make_series(-4, 20.0, -45, 55),
    UT = make_series(-27, 8.0, -50, -6),
    SQ = make_series(-11, 18.0, -46, 46),
    `DRL-RA` = make_series(82, 8.0, 56, 97, 47)
  ),
  LH = list(
    CT = make_series(28, 6.0, 12, 58),
    ET = make_series(-25, 10.0, -50, -1),
    TT = make_series(-8, 7.0, -30, 10),
    UT = make_series(-30, 7.0, -50, -8),
    SQ = make_series(-12, 8.0, -35, 7),
    `DRL-RA` = make_series(42, 7.0, 23, 68)
  ),
  LL = list(
    CT = make_series(31, 7.0, 5, 64),
    ET = make_series(-22, 10.0, -48, 3),
    TT = make_series(-9, 7.0, -32, 10),
    UT = make_series(-28, 8.0, -50, -6),
    SQ = make_series(-13, 8.0, -36, 6),
    `DRL-RA` = make_series(45, 9.0, 8, 67)
  )
)

# 图中星号表示最优的两个基准规则；红叉表示低于 EA 基准的规则。
annotations <- list(
  HH = list(stars = c(1, 2), crosses = c(3, 4, 5)),
  HL = list(stars = c(1, 2), crosses = c(3, 4, 5)),
  LH = list(stars = c(1, 3), crosses = c(2, 3, 4, 5)),
  LL = list(stars = c(1, 3), crosses = c(2, 3, 4, 5))
)

win_without_drl <- list(
  HH = c(EA = 0, CT = 95, ET = 5, TT = 0, UT = 0, SQ = 0),
  HL = c(EA = 0, CT = 95, ET = 5, TT = 0, UT = 0, SQ = 0),
  LH = c(EA = 0, CT = 100, ET = 0, TT = 0, UT = 0, SQ = 0),
  LL = c(EA = 2, CT = 95, ET = 3, TT = 0, UT = 0, SQ = 0)
)

win_with_drl <- list(
  HH = c(EA = 0, CT = 12, ET = 0, TT = 0, UT = 0, SQ = 0, `DRL-RA` = 88),
  HL = c(EA = 1, CT = 15, ET = 0, TT = 0, UT = 0, SQ = 0, `DRL-RA` = 84),
  LH = c(EA = 0, CT = 7, ET = 0, TT = 0, UT = 0, SQ = 0, `DRL-RA` = 93),
  LL = c(EA = 0, CT = 10, ET = 0, TT = 0, UT = 0, SQ = 0, `DRL-RA` = 90)
)

draw_star <- function(x, y, radius_x = 0.13, radius_y = 3.1) {
  angles <- pi / 2 + seq(0, 2 * pi, length.out = 11)[1:10]
  radii_x <- rep(c(radius_x, radius_x * 0.42), 5)
  radii_y <- rep(c(radius_y, radius_y * 0.42), 5)
  polygon(
    x + cos(angles) * radii_x,
    y + sin(angles) * radii_y,
    col = "#FFD51A",
    border = "black",
    lwd = 1.1
  )
}

draw_cross <- function(x, y, radius_x = 0.095, radius_y = 2.3) {
  segments(x - radius_x, y - radius_y, x + radius_x, y + radius_y,
           col = "black", lwd = 3.2)
  segments(x - radius_x, y + radius_y, x + radius_x, y - radius_y,
           col = "black", lwd = 3.2)
  segments(x - radius_x, y - radius_y, x + radius_x, y + radius_y,
           col = "#F00000", lwd = 1.7)
  segments(x - radius_x, y + radius_y, x + radius_x, y - radius_y,
           col = "#F00000", lwd = 1.7)
}

draw_box_panel <- function(scenario, panel_letter, show_y_axis = FALSE) {
  data <- scenario_data[[scenario]]
  par(
    mar = c(3.3, if (show_y_axis) 3.7 else 0.7, 2.0, 0.35),
    mgp = c(2.0, 0.45, 0),
    tcl = -0.22,
    family = font_family,
    xpd = FALSE
  )

  plot(NA, xlim = c(0.45, 6.55), ylim = c(-20, 100), axes = FALSE,
       xlab = "", ylab = "", type = "n")
  rect(0.45, -20, 6.55, 100, col = panel_background, border = NA)
  abline(h = seq(-20, 100, 10), col = grid_color, lwd = 0.55)
  abline(h = 0, col = "#202020", lwd = 0.8)

  boxplot(
    data,
    add = TRUE,
    at = seq_along(data),
    axes = FALSE,
    names = FALSE,
    notch = TRUE,
    boxwex = 0.62,
    col = "white",
    border = "#202020",
    medcol = "#F28E2B",
    medlwd = 1.15,
    boxlwd = 0.95,
    whisklwd = 0.9,
    staplelwd = 0.9,
    outpch = 1,
    outcex = 0.68,
    outlwd = 0.8
  )

  axis(1, at = 1:6, labels = FALSE, lwd = 0.8)
  axis(2, at = seq(-20, 100, 10), labels = if (show_y_axis) seq(-20, 100, 10) else FALSE,
       las = 1, cex.axis = 0.72, lwd = 0.8)
  box(lwd = 0.85)

  # 前五个规则使用常规字重，DRL-RA 使用粗体。
  text(1:5, -24, labels = names(data)[1:5], srt = 25, adj = 1,
       xpd = NA, cex = 0.72)
  text(6, -24, labels = "DRL-RA", srt = 25, adj = 1,
       xpd = NA, cex = 0.72, font = 2)

  if (show_y_axis) {
    mtext("Normalised performance %", side = 2, line = 2.65, cex = 0.72)
  }

  title(main = sprintf("(%s.1) %s", panel_letter, scenario), line = 0.55,
        cex.main = 0.90, font.main = 1)

  drl_mean <- mean(data[["DRL-RA"]])
  abline(h = drl_mean, col = mean_color, lty = 2, lwd = 1.15)
  legend("topleft", inset = 0.025, legend = "mean of DRL-RA",
         col = mean_color, lty = 2, lwd = 1.15,
         bg = "white", box.col = "#BBBBBB", cex = 0.61,
         seg.len = 1.6, x.intersp = 0.55, y.intersp = 0.75)

  star_positions <- annotations[[scenario]]$stars
  cross_positions <- annotations[[scenario]]$crosses
  for (position in star_positions) {
    star_y <- if (position %in% cross_positions) 10 else 0
    draw_star(position, star_y)
  }
  for (position in cross_positions) {
    draw_cross(position, 0)
  }
}

draw_pie_panel <- function(values, panel_title, bold_drl = FALSE) {
  positive <- values[values > 0]
  label_code <- as.character(positive)
  if (bold_drl && "DRL-RA" %in% names(positive)) {
    label_code[names(positive) == "DRL-RA"] <-
      sprintf("bold(%s)", positive[["DRL-RA"]])
  }

  par(mar = c(0.1, 0.1, 1.25, 0.1), family = font_family)
  pie(
    positive,
    labels = parse(text = label_code),
    col = method_colors[names(positive)],
    border = "white",
    lwd = 1.0,
    clockwise = TRUE,
    init.angle = 90,
    radius = 0.76,
    cex = 0.72
  )
  title(main = panel_title, line = 0.18, cex.main = 0.88, font.main = 1)
}

draw_legend_panel <- function() {
  par(mar = c(0.1, 0.4, 0.1, 0.4), family = font_family, xpd = NA)
  plot.new()
  plot.window(xlim = c(0, 1), ylim = c(0, 1))

  legend_names <- names(method_colors)
  legend_x <- c(0.02, 0.16, 0.30, 0.44, 0.02, 0.16, 0.30)
  legend_y <- c(0.79, 0.79, 0.79, 0.79, 0.52, 0.52, 0.52)
  for (index in seq_along(legend_names)) {
    rect(legend_x[index], legend_y[index] - 0.045,
         legend_x[index] + 0.025, legend_y[index] + 0.045,
         col = method_colors[index], border = NA)
    text(legend_x[index] + 0.032, legend_y[index], legend_names[index],
         adj = c(0, 0.5), cex = 0.66,
         font = if (legend_names[index] == "DRL-RA") 2 else 1)
  }
  rect(0.008, 0.40, 0.56, 0.89, border = "#BDBDBD", lwd = 0.7)

  # 在图例中复现星号、红叉及两种胜率口径说明。
  draw_star(0.625, 0.80, radius_x = 0.009, radius_y = 0.065)
  text(0.645, 0.80, "Top two benchmark rules", adj = c(0, 0.5), cex = 0.66)
  draw_cross(0.625, 0.59, radius_x = 0.007, radius_y = 0.045)
  text(0.645, 0.59, "Lower-than-baseline performance", adj = c(0, 0.5), cex = 0.66)
  text(0.60, 0.38, "DRL(\u00D7)", adj = c(0, 0.5), cex = 0.66)
  text(0.68, 0.38, "Result excluding DRL agents", adj = c(0, 0.5), cex = 0.66)
  text(0.60, 0.21, "DRL(\u221A)", adj = c(0, 0.5), cex = 0.66)
  text(0.68, 0.21, "Result including DRL agents", adj = c(0, 0.5), cex = 0.66)

  text(0.01, 0.02, "Figure 6.", col = "#008F87", font = 2,
       adj = c(0, 0), cex = 0.73)
  text(0.082, 0.02,
       "Tardiness performance of RA under four validation scenarios.",
       adj = c(0, 0), cex = 0.73)
}

draw_figure <- function() {
  layout(
    rbind(
      1:4,
      5:8,
      9:12,
      rep(13, 4)
    ),
    heights = c(3.30, 1.55, 1.55, 1.20),
    widths = rep(1, 4)
  )

  scenario_names <- names(scenario_data)
  panel_letters <- letters[1:4]

  for (index in seq_along(scenario_names)) {
    draw_box_panel(
      scenario_names[index],
      panel_letters[index],
      show_y_axis = index == 1
    )
  }

  for (index in seq_along(scenario_names)) {
    draw_pie_panel(
      win_without_drl[[scenario_names[index]]],
      sprintf("(%s.2) Win %%, DRL(\u00D7)", panel_letters[index])
    )
  }

  for (index in seq_along(scenario_names)) {
    draw_pie_panel(
      win_with_drl[[scenario_names[index]]],
      sprintf("(%s.3) Win %%, DRL(\u221A)", panel_letters[index]),
      bold_drl = TRUE
    )
  }

  draw_legend_panel()
}

png(
  paste0(output_stem, ".png"),
  width = 6.5,
  height = 5.5667,
  units = "in",
  res = 300,
  type = "windows",
  family = font_family,
  antialias = "cleartype"
)
draw_figure()
dev.off()

cairo_pdf(
  paste0(output_stem, ".pdf"),
  width = 6.5,
  height = 5.57,
  family = font_family
)
draw_figure()
dev.off()

outputs <- paste0(output_stem, c(".png", ".pdf"))
stopifnot(all(file.exists(outputs)), all(file.info(outputs)$size > 0))
cat(paste(normalizePath(outputs, winslash = "/"), collapse = "\n"), "\n")
