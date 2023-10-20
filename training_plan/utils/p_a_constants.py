""" Contstants and Data for the plan_algo.py file"""

""" Week"""
WEEK = ("mon", "tue", "wed", "thu", "fri", "sat", "sun") 

""" Plan constants """
MIN_DAYS = 90 
MAX_DAYS = 365

""" Basic plans """
BASIC_PLANS = {
    "beginner": {
        "phase1": {
            "mon": 2, 
            "tue": 0, 
            "wed": 2, 
            "thu": 0, 
            "fri": 1, 
            "sat": 6, 
            "sun": 0 
        },
        "phase2": {
            "mon": 2, 
            "tue": 1, 
            "wed": 2, 
            "thu": 3, 
            "fri": 0, 
            "sat": 6, 
            "sun": 2 
        },
        "phase3": {
            "mon": 2, 
            "tue": 5, 
            "wed": 2, 
            "thu": 4, 
            "fri": 0, 
            "sat": 1, 
            "sun": 6 
        }
    },
    "intermediate": {
        "phase1": {
            "mon": 2, 
            "tue": 0, 
            "wed": 2, 
            "thu": 2, 
            "fri": 1, 
            "sat": 6, 
            "sun": 3 
        },
        "phase2": {
            "mon": 2, 
            "tue": 2, 
            "wed": 2, 
            "thu": 3, 
            "fri": 0, 
            "sat": 6, 
            "sun": 2 
        },
        "phase3": {
            "mon": 2, 
            "tue": 5, 
            "wed": 2, 
            "thu": 4, 
            "fri": 0, 
            "sat": 1, 
            "sun": 6 
        }
    },
    "advanced": {
        "phase1": {
            "mon": 2, 
            "tue": 0, 
            "wed": 2, 
            "thu": 2, 
            "fri": 2, 
            "sat": 6, 
            "sun": 3 
        },
        "phase2": {
            "mon": 2, 
            "tue": 2, 
            "wed": 2, 
            "thu": 3, 
            "fri": 0, 
            "sat": 6, 
            "sun": 2 
        },
        "phase3": {
            "mon": 2, 
            "tue": 5, 
            "wed": 2, 
            "thu": 4, 
            "fri": 0, 
            "sat": 1, 
            "sun": 6 
        }
    },
}

""" Default runs """
DEFAULT_RUNS = {
    0: {
        "name": "Rest",
        "zone": {
            "int": 0,
            "desc": "Rest"
        },
        "feel": "No run today! :("
    },
    1: {
        "name": "Recovery Run",
        "zone": {
            "int": 1,
            "desc": "Recovery"
        },
        "feel": "Light and easy; you could easily hold a conversation",
        "distance": {
            "beginner": {
                "phase1": {
                    "low": 1,
                    "high": 4
                },
                "phase2": {
                    "low": 2, 
                    "high": 5
                },
                "phase3": {
                    "low": 5, 
                    "high": 5
                }
            },
            "intermediate": {
                "phase1": {
                    "low": 2,
                    "high": 5
                },
                "phase2": {
                    "low": 3, 
                    "high": 6
                },
                "phase3": {
                    "low": 6,
                    "high": 6
                }
            },
            "advanced": {
                "phase1": {
                    "low": 4,
                    "high": 8
                },
                "phase2": {
                    "low": 5, 
                    "high": 8
                },
                "phase3": {
                    "low": 8,
                    "high": 8
                }
            },
        },
        "first_duration": {
            "beginner": 10,
            "intermediate": 15,
            "advanced": 50
        }
    },
    2: {
        "name": "Base Run",
        "zone": {
            "int": 2,
            "desc": "Base"
        },
        "feel": "You're working but you can still chat comfortably and maintain the pase without feeling exhausted",
        "distance": {
            "beginner": {
                "phase1": {
                    "low": 2,
                    "high": 10
                },
                "phase2": {
                    "low": 8, 
                    "high": 15
                },
                "phase3": {
                    "low": 16,
                    "high": 16
                }
            },
            "intermediate": {
                "phase1": {
                    "low": 8,
                    "high": 12
                },
                "phase2": {
                    "low": 12, 
                    "high": 16
                },
                "phase3": {
                    "low": 16,
                    "high": 16
                }
            },
            "advanced": {
                "phase1": {
                    "low": 10,
                    "high": 15
                },
                "phase2": {
                    "low": 12, 
                    "high": 16
                },
                "phase3": {
                    "low": 16,
                    "high": 16
                }
            },
        },
        "first_duration": {
            "beginner": 10,
            "intermediate": 35,
            "advanced": 50
        }
    },
    3: {
        "name": "Long Tempo Run",
        "zone": {
            "int": 3,
            "desc": "Hard"
        },
        "feel": "Pushing the pace, you could carry on for longer but it's much harder to; can't sustain a conversation",
        "distance": {
            "beginner": {
                "phase1": {
                    "low": 1,
                    "high": 10
                },
                "phase2": {
                    "low": 8, 
                    "high": 12
                },
                "phase3": {
                    "low": 12,
                    "high": 12
                }
            },
            "intermediate": {
                "phase1": {
                    "low": 5,
                    "high": 12
                },
                "phase2": {
                    "low": 10, 
                    "high": 15
                },
                "phase3": {
                    "low": 15,
                    "high": 15
                }
            },
            "advanced": {
                "phase1": {
                    "low": 5,
                    "high": 12
                },
                "phase2": {
                    "low": 10, 
                    "high": 16
                },
                "phase3": {
                    "low": 16,
                    "high": 16
                }
            },
        },
        "first_duration": {
            "beginner": 10,
            "intermediate": 25,
            "advanced": 20
        }
    },
    4: {
        "name": "Harder Tempo Run",
        "zone": {
            "int": 4,
            "desc": "Hard"
        },
        "feel": "A tough workout, you should have nothing left by the end of the run!",
        "distance": {
            "beginner": {
                "phase1": {
                    "low": 1,
                    "high": 5
                },
                "phase2": {
                    "low": 3, 
                    "high": 8
                },
                "phase3": {
                    "low": 8,
                    "high": 8
                }
            },
            "intermediate": {
                "phase1": {
                    "low": 2,
                    "high": 5
                },
                "phase2": {
                    "low": 5, 
                    "high": 10
                },
                "phase3": {
                    "low": 10,
                    "high": 10
                }
            },
            "advanced": {
                "phase1": {
                    "low": 5,
                    "high": 10
                },
                "phase2": {
                    "low": 10, 
                    "high": 12
                },
                "phase3": {
                    "low": 12,
                    "high": 12
                }
            },
        },
        "first_duration": {
            "beginner": 50,
            "intermediate": 50,
            "advanced": 50
        }
    },
    5: {
        "name": "Interval Runs",
        "zone": {
            "int": 5,
            "desc": "Max Effort"
        },
        "feel": "Pace yourself over all the intervals but give it everything you have! Push yourself!",
        "on": 4,
        "off": 4,
        "sets": {
            "beginner": {
                "phase1": {
                    "low": 1,
                    "high": 3
                },
                "phase2": {
                    "low": 2,
                    "high": 4
                },
                "phase3": {
                    "low": 2,
                    "high": 6
                },
            },
            "intermediate": {
                "phase1": {
                    "low": 1,
                    "high": 4
                },
                "phase2": {
                    "low": 3,
                    "high": 5
                },
                "phase3": {
                    "low": 4,
                    "high": 8
                },
            },
            "advanced": {
                "phase1": {
                    "low": 3,
                    "high": 5
                },
                "phase2": {
                    "low": 4,
                    "high": 6
                },
                "phase3": {
                    "low": 6,
                    "high": 8
                },
            }
        },
        "first_duration": {
            "beginner": 16,
            "intermediate": 32,
            "advanced": 48
        }
    },
    6: {
        "name": "Long Base Run",
        "zone": {
            "int": 2,
            "desc": "Base"
        },
        "feel": "You're working but you can still chat comfortably and maintain the pase without feeling exhausted",
        "distance": {
            "beginner": {
                "phase1": {
                    "low": 5,
                    "high": 15
                },
                "phase2": {
                    "low": 15, 
                    "high": 22
                },
                "phase3": {
                    "low": 22, 
                    "high": 36
                }
            },
            "intermediate": {
                "phase1": {
                    "low": 12,
                    "high": 20
                },
                "phase2": {
                    "low": 18, 
                    "high": 24
                },
                "phase3": {
                    "low": 22, 
                    "high": 36
                }
            },
            "advanced": {
                "phase1": {
                    "low": 12,
                    "high": 20
                },
                "phase2": {
                    "low": 18, 
                    "high": 26
                },
                "phase3": {
                    "low": 22, 
                    "high": 36
                }
            },
        },
        "first_duration": {
            "beginner": 35,
            "intermediate": 70,
            "advanced": 60
        }
    }
}

""" Scaling factors """
SCALING_FACTORS = {
    "beginner": {
        "duration": 0.4,
        "distance": 0.4,
        "on": 0.4,
        "off": 1.6,
        "sets": 0.5
    },
    "intermediate": {
        "duration": 1,
        "distance": 1,
        "on": 1,
        "off": 1,
        "sets": 1
    },
    "advanced": {
        "duration": 1.2,
        "distance": 1.2,
        "on": 1.2,
        "off": 0.8,
        "sets": 1.2
    }
}

""" Feedback adjustments """
FEEDBACK_ADJUSTMENTS = {
    "too_easy": 1.1,   # Increase by 10%
    "just_right": 1,  # No change
    "too_hard": 0.9   # Decrease by 10%
}