#!/usr/bin/env python
# coding: utf-8

from typing import Dict, Optional

import pandas

from evidently.model.widget import BaseWidgetInfo, AlertStats
from evidently.widgets.widget import Widget


class BarWidget(Widget):

    wi: Optional[BaseWidgetInfo]

    def __init__(self, title: str):
        super().__init__()
        self.wi = None
        self.title = title

    def analyzers(self):
        return []

    def calculate(self, reference_data: pandas.DataFrame, production_data: pandas.DataFrame, column_mapping: Dict,
                  analyzes_results):
        self.wi = BaseWidgetInfo(
            type="big_graph",
            title=self.title,
            size=2,
            params={
                "data": [
                    {
                        "marker": {
                            "color": "#ed0400"
                        },
                        "type": "bar",
                        "x": reference_data[0].tolist(),
                        "y": reference_data[1].tolist()
                    }
                ],
                "layout": {
                    "template": {
                        "data": {
                            "bar": [
                                {
                                    "error_x": {
                                        "color": "#2a3f5f"
                                    },
                                    "error_y": {
                                        "color": "#2a3f5f"
                                    },
                                    "marker": {
                                        "line": {
                                            "color": "#E5ECF6",
                                            "width": 0.5
                                        }
                                    },
                                    "type": "bar"
                                }
                            ],
                            "barpolar": [
                                {
                                    "marker": {
                                        "line": {
                                            "color": "#E5ECF6",
                                            "width": 0.5
                                        }
                                    },
                                    "type": "barpolar"
                                }
                            ],
                            "carpet": [
                                {
                                    "aaxis": {
                                        "endlinecolor": "#2a3f5f",
                                        "gridcolor": "white",
                                        "linecolor": "white",
                                        "minorgridcolor": "white",
                                        "startlinecolor": "#2a3f5f"
                                    },
                                    "baxis": {
                                        "endlinecolor": "#2a3f5f",
                                        "gridcolor": "white",
                                        "linecolor": "white",
                                        "minorgridcolor": "white",
                                        "startlinecolor": "#2a3f5f"
                                    },
                                    "type": "carpet"
                                }
                            ],
                            "choropleth": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "type": "choropleth"
                                }
                            ],
                            "contour": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ],
                                    "type": "contour"
                                }
                            ],
                            "contourcarpet": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "type": "contourcarpet"
                                }
                            ],
                            "heatmap": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ],
                                    "type": "heatmap"
                                }
                            ],
                            "heatmapgl": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ],
                                    "type": "heatmapgl"
                                }
                            ],
                            "histogram": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "histogram"
                                }
                            ],
                            "histogram2d": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ],
                                    "type": "histogram2d"
                                }
                            ],
                            "histogram2dcontour": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ],
                                    "type": "histogram2dcontour"
                                }
                            ],
                            "mesh3d": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "type": "mesh3d"
                                }
                            ],
                            "parcoords": [
                                {
                                    "line": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "parcoords"
                                }
                            ],
                            "pie": [
                                {
                                    "automargin": True,
                                    "type": "pie"
                                }
                            ],
                            "scatter": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scatter"
                                }
                            ],
                            "scatter3d": [
                                {
                                    "line": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scatter3d"
                                }
                            ],
                            "scattercarpet": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scattercarpet"
                                }
                            ],
                            "scattergeo": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scattergeo"
                                }
                            ],
                            "scattergl": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scattergl"
                                }
                            ],
                            "scattermapbox": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scattermapbox"
                                }
                            ],
                            "scatterpolar": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scatterpolar"
                                }
                            ],
                            "scatterpolargl": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scatterpolargl"
                                }
                            ],
                            "scatterternary": [
                                {
                                    "marker": {
                                        "colorbar": {
                                            "outlinewidth": 0,
                                            "ticks": ""
                                        }
                                    },
                                    "type": "scatterternary"
                                }
                            ],
                            "surface": [
                                {
                                    "colorbar": {
                                        "outlinewidth": 0,
                                        "ticks": ""
                                    },
                                    "colorscale": [
                                        [
                                            0.0,
                                            "#0d0887"
                                        ],
                                        [
                                            0.1111111111111111,
                                            "#46039f"
                                        ],
                                        [
                                            0.2222222222222222,
                                            "#7201a8"
                                        ],
                                        [
                                            0.3333333333333333,
                                            "#9c179e"
                                        ],
                                        [
                                            0.4444444444444444,
                                            "#bd3786"
                                        ],
                                        [
                                            0.5555555555555556,
                                            "#d8576b"
                                        ],
                                        [
                                            0.6666666666666666,
                                            "#ed7953"
                                        ],
                                        [
                                            0.7777777777777778,
                                            "#fb9f3a"
                                        ],
                                        [
                                            0.8888888888888888,
                                            "#fdca26"
                                        ],
                                        [
                                            1.0,
                                            "#f0f921"
                                        ]
                                    ],
                                    "type": "surface"
                                }
                            ],
                            "table": [
                                {
                                    "cells": {
                                        "fill": {
                                            "color": "#EBF0F8"
                                        },
                                        "line": {
                                            "color": "white"
                                        }
                                    },
                                    "header": {
                                        "fill": {
                                            "color": "#C8D4E3"
                                        },
                                        "line": {
                                            "color": "white"
                                        }
                                    },
                                    "type": "table"
                                }
                            ]
                        },
                        "layout": {
                            "annotationdefaults": {
                                "arrowcolor": "#2a3f5f",
                                "arrowhead": 0,
                                "arrowwidth": 1
                            },
                            "coloraxis": {
                                "colorbar": {
                                    "outlinewidth": 0,
                                    "ticks": ""
                                }
                            },
                            "colorscale": {
                                "diverging": [
                                    [
                                        0,
                                        "#8e0152"
                                    ],
                                    [
                                        0.1,
                                        "#c51b7d"
                                    ],
                                    [
                                        0.2,
                                        "#de77ae"
                                    ],
                                    [
                                        0.3,
                                        "#f1b6da"
                                    ],
                                    [
                                        0.4,
                                        "#fde0ef"
                                    ],
                                    [
                                        0.5,
                                        "#f7f7f7"
                                    ],
                                    [
                                        0.6,
                                        "#e6f5d0"
                                    ],
                                    [
                                        0.7,
                                        "#b8e186"
                                    ],
                                    [
                                        0.8,
                                        "#7fbc41"
                                    ],
                                    [
                                        0.9,
                                        "#4d9221"
                                    ],
                                    [
                                        1,
                                        "#276419"
                                    ]
                                ],
                                "sequential": [
                                    [
                                        0.0,
                                        "#0d0887"
                                    ],
                                    [
                                        0.1111111111111111,
                                        "#46039f"
                                    ],
                                    [
                                        0.2222222222222222,
                                        "#7201a8"
                                    ],
                                    [
                                        0.3333333333333333,
                                        "#9c179e"
                                    ],
                                    [
                                        0.4444444444444444,
                                        "#bd3786"
                                    ],
                                    [
                                        0.5555555555555556,
                                        "#d8576b"
                                    ],
                                    [
                                        0.6666666666666666,
                                        "#ed7953"
                                    ],
                                    [
                                        0.7777777777777778,
                                        "#fb9f3a"
                                    ],
                                    [
                                        0.8888888888888888,
                                        "#fdca26"
                                    ],
                                    [
                                        1.0,
                                        "#f0f921"
                                    ]
                                ],
                                "sequentialminus": [
                                    [
                                        0.0,
                                        "#0d0887"
                                    ],
                                    [
                                        0.1111111111111111,
                                        "#46039f"
                                    ],
                                    [
                                        0.2222222222222222,
                                        "#7201a8"
                                    ],
                                    [
                                        0.3333333333333333,
                                        "#9c179e"
                                    ],
                                    [
                                        0.4444444444444444,
                                        "#bd3786"
                                    ],
                                    [
                                        0.5555555555555556,
                                        "#d8576b"
                                    ],
                                    [
                                        0.6666666666666666,
                                        "#ed7953"
                                    ],
                                    [
                                        0.7777777777777778,
                                        "#fb9f3a"
                                    ],
                                    [
                                        0.8888888888888888,
                                        "#fdca26"
                                    ],
                                    [
                                        1.0,
                                        "#f0f921"
                                    ]
                                ]
                            },
                            "colorway": [
                                "#636efa",
                                "#EF553B",
                                "#00cc96",
                                "#ab63fa",
                                "#FFA15A",
                                "#19d3f3",
                                "#FF6692",
                                "#B6E880",
                                "#FF97FF",
                                "#FECB52"
                            ],
                            "font": {
                                "color": "#2a3f5f"
                            },
                            "geo": {
                                "bgcolor": "white",
                                "lakecolor": "white",
                                "landcolor": "#E5ECF6",
                                "showlakes": True,
                                "showland": True,
                                "subunitcolor": "white"
                            },
                            "hoverlabel": {
                                "align": "left"
                            },
                            "hovermode": "closest",
                            "mapbox": {
                                "style": "light"
                            },
                            "paper_bgcolor": "white",
                            "plot_bgcolor": "#E5ECF6",
                            "polar": {
                                "angularaxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                },
                                "bgcolor": "#E5ECF6",
                                "radialaxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                }
                            },
                            "scene": {
                                "xaxis": {
                                    "backgroundcolor": "#E5ECF6",
                                    "gridcolor": "white",
                                    "gridwidth": 2,
                                    "linecolor": "white",
                                    "showbackground": True,
                                    "ticks": "",
                                    "zerolinecolor": "white"
                                },
                                "yaxis": {
                                    "backgroundcolor": "#E5ECF6",
                                    "gridcolor": "white",
                                    "gridwidth": 2,
                                    "linecolor": "white",
                                    "showbackground": True,
                                    "ticks": "",
                                    "zerolinecolor": "white"
                                },
                                "zaxis": {
                                    "backgroundcolor": "#E5ECF6",
                                    "gridcolor": "white",
                                    "gridwidth": 2,
                                    "linecolor": "white",
                                    "showbackground": True,
                                    "ticks": "",
                                    "zerolinecolor": "white"
                                }
                            },
                            "shapedefaults": {
                                "line": {
                                    "color": "#2a3f5f"
                                }
                            },
                            "ternary": {
                                "aaxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                },
                                "baxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                },
                                "bgcolor": "#E5ECF6",
                                "caxis": {
                                    "gridcolor": "white",
                                    "linecolor": "white",
                                    "ticks": ""
                                }
                            },
                            "title": {
                                "x": 0.05
                            },
                            "xaxis": {
                                "automargin": True,
                                "gridcolor": "white",
                                "linecolor": "white",
                                "ticks": "",
                                "title": {
                                    "standoff": 15
                                },
                                "zerolinecolor": "white",
                                "zerolinewidth": 2
                            },
                            "yaxis": {
                                "automargin": True,
                                "gridcolor": "white",
                                "linecolor": "white",
                                "ticks": "",
                                "title": {
                                    "standoff": 15
                                },
                                "zerolinecolor": "white",
                                "zerolinewidth": 2
                            }
                        }
                    },
                    "xaxis": {
                        "title": {
                            "text": "Features"
                        }
                    },
                    "yaxis": {
                        "range": [
                            -1,
                            1
                        ],
                        "showticklabels": True,
                        "title": {
                            "text": "Correlation"
                        }
                    }
                }
            },
            alerts=[],
            insights=[],
            details="",
            alertsPosition="row",
            alertStats=AlertStats(),
            additionalGraphs=[],
        )

    def get_info(self) -> BaseWidgetInfo:
        if self.wi:
            return self.wi
        raise ValueError("no widget info provided")
