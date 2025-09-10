## Full Panel JSON

<img width="1139" height="376" alt="Zrzut ekranu 2025-09-7 o 22 03 29" src="https://github.com/user-attachments/assets/3ef37f8f-b4a3-4853-9cfb-2d70de0ba100" />

Below is the full configuration for a Grafana panel that displays the price history of RTX 5090 graphics cards over time.

This panel is a **time series** visualization that reads data from a MySQL datasource and plots product prices. It supports multiple products and shops, showing each combination as a separate metric.

```json
{
  "id": 4,
  "type": "timeseries",
  "title": "RTX 5090 Prices",
  "gridPos": {
    "x": 0,
    "y": 0,
    "h": 10,
    "w": 24
  },
  "fieldConfig": {
    "defaults": {
      "custom": {
        "drawStyle": "line",
        "lineInterpolation": "linear",
        "barAlignment": 0,
        "barWidthFactor": 0.6,
        "lineWidth": 1,
        "fillOpacity": 0,
        "gradientMode": "none",
        "spanNulls": true,
        "insertNulls": false,
        "showPoints": "auto",
        "pointSize": 5,
        "stacking": {
          "mode": "none",
          "group": "A"
        },
        "axisPlacement": "auto",
        "axisLabel": "Price",
        "axisColorMode": "text",
        "axisBorderShow": false,
        "scaleDistribution": {
          "type": "linear"
        },
        "axisCenteredZero": false,
        "hideFrom": {
          "tooltip": false,
          "viz": false,
          "legend": false
        },
        "thresholdsStyle": {
          "mode": "off"
        },
        "axisGridShow": true
      },
      "color": {
        "mode": "palette-classic"
      },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "color": "green", "value": null },
          { "color": "red", "value": 80 }
        ]
      },
      "unit": "locale"
    },
    "overrides": []
  },
  "pluginVersion": "11.4.0",
  "targets": [
    {
      "dataset": "easy_price_monitor",
      "datasource": {
        "type": "mysql",
        "uid": "bexd93voy11j4b"
      },
      "editorMode": "code",
      "format": "time_series",
      "rawQuery": true,
      "rawSql": "SELECT \n  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,\n  pr.price AS value,\n  CONCAT(SUBSTRING_INDEX(p.name, ' ', 5), ' - ', s.name) AS metric\n FROM prices pr JOIN shops s ON s.id = pr.shop_id JOIN products p ON p.id = pr.product_id WHERE $__timeFilter(pr.timestamp) AND pr.product_id IN (7,8,9) ORDER BY pr.timestamp;",
      "refId": "A"
    }
  ],
  "datasource": {
    "type": "mysql",
    "uid": "bexd93voy11j4b"
  },
  "options": {
    "tooltip": {
      "mode": "single",
      "sort": "none"
    },
    "legend": {
      "showLegend": true,
      "displayMode": "table",
      "placement": "bottom",
      "calcs": [
        "lastNotNull",
        "min",
        "max"
      ]
    }
  }
}
```

---

## Query Example

Here is the SQL query used for this panel. It fetches the timestamp, price, and product-shop combination as a single metric for multiple products:

```mysql
SELECT 
  UNIX_TIMESTAMP(pr.timestamp) AS time_sec,
  pr.price AS value,
  CONCAT(SUBSTRING_INDEX(p.name, ' ', 5), ' - ', s.name) AS metric
FROM prices pr
JOIN shops s ON s.id = pr.shop_id
JOIN products p ON p.id = pr.product_id
WHERE $__timeFilter(pr.timestamp)
  AND pr.product_id IN (7,8,9)
ORDER BY pr.timestamp;
```
**Make sure to select format to `Time Series`**

<img width="857" height="140" alt="Zrzut ekranu 2025-09-10 o 21 00 28" src="https://github.com/user-attachments/assets/5313e180-fe91-489e-a4db-7f9352845f23" />

**Notes:**

* `time_sec` – Timestamp in seconds, required for Grafana time series panels.
* `value` – Product price.
* `metric` – Combination of product name and shop name (first 5 words of the product name) used for grouping in Grafana.
* `$__timeFilter(pr.timestamp)` – Grafana macro for filtering data according to the selected dashboard time range.

---

This configuration can be easily extended to include more products or shops. Adjust the `rawSql` query or the `product_id` list to monitor additional items.
