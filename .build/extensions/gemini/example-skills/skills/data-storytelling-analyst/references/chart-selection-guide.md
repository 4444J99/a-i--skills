# Chart Selection Guide

Choose the right visualization for your data story.

## By Data Relationship

### Comparison

Comparing values across categories or time.

| Chart Type | Best For | Avoid When |
|------------|----------|------------|
| Bar chart | Few categories (<12), exact values matter | Too many categories |
| Grouped bar | Comparing subcategories | >4 groups per category |
| Horizontal bar | Long category names | Showing time series |
| Lollipop | Modern bar alternative | Tradition expected |
| Dot plot | Precise comparison | Large datasets |

### Distribution

Understanding how values spread.

| Chart Type | Best For | Avoid When |
|------------|----------|------------|
| Histogram | Continuous data shape | Categorical data |
| Box plot | Comparing distributions | Non-technical audience |
| Violin | Distribution + density | Few data points |
| Swarm/beeswarm | Small datasets, exact points | >500 points |
| Density plot | Smooth distribution shape | Precision needed |

### Composition

Parts of a whole.

| Chart Type | Best For | Avoid When |
|------------|----------|------------|
| Pie chart | 2-5 segments, shares obvious | >5 segments, small differences |
| Donut | Same as pie, space for metric | Precision needed |
| Stacked bar | Composition over time | Many components |
| Treemap | Hierarchical parts | No hierarchy |
| Waffle | Making percentages tangible | Precise values needed |

### Trend/Change

Values over time.

| Chart Type | Best For | Avoid When |
|------------|----------|------------|
| Line chart | Continuous time series | Few time points |
| Area chart | Volume/magnitude over time | Multiple overlapping series |
| Stacked area | Composition trend | Comparing individual series |
| Slope chart | Before/after comparison | >10 items |
| Sparklines | Inline trends | Detail needed |

### Correlation

Relationships between variables.

| Chart Type | Best For | Avoid When |
|------------|----------|------------|
| Scatter plot | Two continuous variables | Overlapping points |
| Bubble chart | Three variables | Fourth variable needed |
| Heatmap | Matrix of values | Few categories |
| Connected scatter | Change over two dimensions | No temporal order |

### Flow

Movement or process.

| Chart Type | Best For | Avoid When |
|------------|----------|------------|
| Sankey | Flow between stages | Simple two-point flow |
| Chord | Circular relationships | Linear flow |
| Funnel | Sequential stages | Non-sequential data |
| Waterfall | Cumulative changes | No intermediate steps |

## Quick Decision Tree

```
What story are you telling?
│
├─ Comparing values?
│  ├─ Over time? → Line chart
│  ├─ Across categories? → Bar chart
│  └─ Multiple dimensions? → Grouped bar / Small multiples
│
├─ Showing parts of whole?
│  ├─ Few parts (<6)? → Pie/Donut
│  ├─ Hierarchical? → Treemap
│  └─ Over time? → Stacked bar/area
│
├─ Showing distribution?
│  ├─ One variable? → Histogram
│  ├─ Compare groups? → Box plot / Violin
│  └─ Show individual points? → Swarm / Strip
│
├─ Showing relationship?
│  ├─ Two variables? → Scatter plot
│  ├─ Three variables? → Bubble chart
│  └─ Many pairs? → Heatmap
│
└─ Showing flow/process?
   ├─ Sequential stages? → Funnel / Sankey
   └─ Cumulative change? → Waterfall
```

## Audience Considerations

### Executive Summary

- Simple: bar, line, pie
- Large: single number metrics
- Avoid: complex, interactive

### Technical Team

- Detailed: scatter, box plot
- Precise: actual values, error bars
- Interactive: drill-down capability

### General Public

- Familiar: bar, line, pie
- Annotated: clear labels, context
- Avoid: statistical (violin, box plot)

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| 3D charts | Distorts values | Use 2D |
| Dual axis | Misleading correlation | Two charts |
| Truncated axis | Exaggerates difference | Start at zero |
| Rainbow colors | No meaning | Use sequential palette |
| Too much data | Overwhelming | Aggregate or filter |
| Missing context | Unclear significance | Add reference lines |

## Annotation Principles

1. **Title**: State the insight, not description
   - Bad: "Sales by Region"
   - Good: "West Region Leads with 42% of Total Sales"

2. **Direct labels** > Legend when possible

3. **Reference lines** for context (average, target, benchmark)

4. **Callouts** for key data points

5. **Source** always included
