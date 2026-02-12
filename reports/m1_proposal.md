# Section 1: Motivation and Purpose  

Dietary shifts toward healthier patterns are often discussed in relation to public health and environmental goals, but adoption can be limited when healthier diets are more expensive or unaffordable for some populations (Springmann et al., 2021). High food prices can also limit people’s ability to obtain nutrient-adequate diets, which is why many policies and programs focus on making nutritious foods more affordable (Bai, Herforth, & Masters, 2022). Together, this motivates a need for clear, comparable evidence on how healthy diet costs differ across places and change over time.  

Our dataset addresses this by providing daily and annualized costs of a healthy diet in PPP-adjusted USD, enabling meaningful cross-country comparisons. It also includes component costs (for example, fruits and vegetables) to help users explore what contributes to overall diet cost.  

The dashboard is intended for policy analysts, public health researchers, international development organizations, and members of the general public who want to understand disparities in healthy diet affordability and how those disparities vary by region and over time. The goal is to support evidence-based decision making by making cross-country differences, trends, and cost drivers easy to explore.  

The dashboard will allow users to:

- Compare countries within and across regions  
- Track trends over time from 2017 to 2024  
- Examine cost components and their contribution to total cost  
- Identify countries classified as high, medium, or low cost  

---

# Section 2: Description of the Data  

The dataset contains 1,379 records relating to the cost of foods by country and by year. The data tracks the daily cost of healthy food for each of the 175 countries in the dataset across 2017 to 2024.  

These costs are measured in Purchasing Power Parity (PPP), which is a normalized currency that accounts for general costs of living for each country. This means that, regardless of currency conversion, a basket of goods in USD will have the same PPP as a similar basket in INR. This allows an apples-to-apples comparison of prices.  

The dataset includes specific variables that track the costs of vegetables and fruits, namely `cost_vegetables_ppp_usd` and `cost_fruits_ppp_usd`. However, these values are sparse and should be used primarily for validation.  

The main metric tracked in this dashboard is `cost_healthy_diet_ppp_usd`. This column is complete with no missing data.  

The ordinal variable `cost_category` contains the final classification of the data and consists of values "High cost" and "Low Cost". About 1% of these classifications are missing and will need to be addressed.  

---

# Section 3: Research Questions & Usage Scenario  

## Usage Scenario

A policy analyst at an international development organization is preparing a regional briefing on food affordability. They need to identify which countries have the highest costs of a healthy diet, how those costs have changed from 2017 to 2024, and whether certain regions are experiencing faster increases than others. They also want to understand whether fruit and vegetable costs contribute substantially to total diet cost in selected countries.  

Using the dashboard, the analyst filters by region, compares countries within that region, examines time trends in `cost_healthy_diet_ppp_usd`, and checks `cost_category` classifications to quickly identify high-cost contexts. They may also review component costs to contextualize differences across countries. The dashboard supports rapid comparison and evidence synthesis for reporting and policy discussion.  

## Research Questions

- How does the cost of a healthy diet (`cost_healthy_diet_ppp_usd`) vary across countries and regions?  
- How have healthy diet costs changed over time from 2017 to 2024?  
- Which regions or countries consistently fall into high-cost versus low-cost categories?  
- To what extent do fruit and vegetable costs contribute to overall healthy diet cost in selected countries?  

## User Stories

- As a policy analyst, I want to compare healthy diet costs across countries within a region so that I can identify which countries face relatively higher affordability challenges.  
- As a public health researcher, I want to examine trends over time in healthy diet costs so that I can assess whether affordability is improving or worsening between 2017 and 2024.  
- As a development practitioner, I want to explore the contribution of fruits and vegetables to total diet cost so that I can better understand potential drivers of high overall costs.  

## Jobs to Be Done

- When preparing a regional or global report, help me quickly identify high-cost countries and compare them across regions so that I can support evidence-based recommendations.  
- When evaluating changes over time, help me visualize trends in healthy diet costs so that I can detect patterns, increases, or relative stability.  
- When exploring cost drivers, help me break down total diet cost into components so that I can better interpret cross-country differences.  

---

# Section 4: Exploratory Data Analysis  

TODO  

---

# Section 5: App Sketch & Description  

TODO  

---

# Section 6: References  

Bai, Y., Herforth, A., & Masters, W. A. (2022). Global variation in the cost of a nutrient-adequate diet by population group: An observational study. *The Lancet Planetary Health, 6*(1), e19–e28. https://doi.org/10.1016/S2542-5196(21)00285-0  

Springmann, M., Clark, M. A., Rayner, M., Scarborough, P., & Webb, P. (2021). The global and regional costs of healthy and sustainable dietary patterns: a modelling study. *The Lancet Planetary Health, 5*(11), e797–e807. https://doi.org/10.1016/s2542-5196(21)00251-5  
