import plotly.express as px

def get_color_scheme(style):
    if style == "다크 테마":
        return px.colors.sequential.Plasma, "#121212", "white"
    elif style == "모던 블루":
        return px.colors.sequential.Blues, "#f8f9fa", "#0f52ba"
    elif style == "미니멀리스트":
        return px.colors.sequential.Greys, "white", "#333333"
    elif style == "HR 특화":
        return px.colors.sequential.Teal, "#f0f8ff", "#006064"
    else:
        return px.colors.qualitative.Plotly, "white", "#333333" 