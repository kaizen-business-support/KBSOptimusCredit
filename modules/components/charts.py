"""
Composants graphiques pour l'analyse financière
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

def create_radar_chart(scores, categories=None):
    """Crée un graphique radar des performances"""
    if categories is None:
        categories = ['Liquidité', 'Solvabilité', 'Rentabilité', 'Activité', 'Gestion']
    
    # Valeurs normalisées sur 10
    values = [
        scores.get('liquidite', 0) / 40 * 10,
        scores.get('solvabilite', 0) / 40 * 10,
        scores.get('rentabilite', 0) / 30 * 10,
        scores.get('activite', 0) / 15 * 10,
        scores.get('gestion', 0) / 15 * 10
    ]
    
    fig = go.Figure()
    
    # Performance actuelle
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name='Performance',
        line_color='rgb(46, 125, 50)',
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
    # Objectif (score parfait)
    fig.add_trace(go.Scatterpolar(
        r=[10, 10, 10, 10, 10, 10],
        theta=categories + [categories[0]],
        fill='tonext',
        name='Objectif (100%)',
        line_color='rgb(211, 47, 47)',
        fillcolor='rgba(244, 67, 54, 0.1)',
        line_dash='dash'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
                tickvals=[0, 2, 4, 6, 8, 10]
            )),
        showlegend=True,
        title="Performance par Catégorie",
        height=500
    )
    
    return fig

def create_waterfall_chart(data):
    """Crée un graphique waterfall des flux de trésorerie"""
    fig = go.Figure(go.Waterfall(
        name="Flux de Trésorerie",
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Trésorerie Ouverture", "Flux Opérationnels", "Flux Investissement", "Flux Financement", "Trésorerie Clôture"],
        y=[
            data.get('tresorerie_ouverture', 0),
            data.get('flux_activites_operationnelles', 0),
            data.get('flux_activites_investissement', 0),
            data.get('flux_activites_financement', 0),
            data.get('tresorerie_cloture', 0)
        ],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title="Évolution de la Trésorerie",
        height=400,
        yaxis_title="Montant (FCFA)"
    )
    
    return fig

def create_performance_bars(ratios, secteur_data=None):
    """Crée un graphique en barres des performances vs secteur"""
    if secteur_data is None:
        secteur_data = {}
    
    # Ratios clés à afficher
    key_ratios = [
        ('ratio_liquidite_generale', 'Liquidité Générale'),
        ('roe', 'ROE (%)'),
        ('marge_nette', 'Marge Nette (%)'),
        ('rotation_stocks', 'Rotation Stocks')
    ]
    
    categories = []
    entreprise_values = []
    secteur_medians = []
    
    for ratio_key, ratio_name in key_ratios:
        if ratio_key in ratios:
            categories.append(ratio_name)
            entreprise_values.append(ratios[ratio_key])
            
            # Valeur sectorielle médiane si disponible
            if ratio_key in secteur_data:
                secteur_medians.append(secteur_data[ratio_key].get('median', 0))
            else:
                secteur_medians.append(0)
    
    fig = go.Figure()
    
    # Barres entreprise
    fig.add_trace(go.Bar(
        name='Votre Entreprise',
        x=categories,
        y=entreprise_values,
        marker_color='lightblue'
    ))
    
    # Barres secteur (si données disponibles)
    if any(secteur_medians):
        fig.add_trace(go.Bar(
            name='Médiane Secteur',
            x=categories,
            y=secteur_medians,
            marker_color='orange',
            opacity=0.7
        ))
    
    fig.update_layout(
        title="Comparaison avec le Secteur",
        barmode='group',
        height=400,
        yaxis_title="Valeur"
    )
    
    return fig

def create_income_statement_chart(data):
    """Crée un graphique des soldes intermédiaires de gestion"""
    categories = ['CA', 'Valeur Ajoutée', 'EBE', 'Résultat Exploitation', 'Résultat Net']
    values = [
        data.get('chiffre_affaires', 0),
        data.get('valeur_ajoutee', 0),
        data.get('excedent_brut', 0),
        data.get('resultat_exploitation', 0),
        data.get('resultat_net', 0)
    ]
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categories,
        y=values,
        marker_color=colors,
        name='Soldes Intermédiaires'
    ))
    
    fig.update_layout(
        title="Soldes Intermédiaires de Gestion",
        xaxis_title="Indicateurs",
        yaxis_title="Montant (FCFA)",
        height=400
    )
    
    return fig

def create_balance_sheet_structure(data):
    """Crée un graphique de structure du bilan"""
    # Actif
    actif_data = {
        'Immobilisations': data.get('immobilisations_nettes', 0),
        'Actif Circulant': data.get('total_actif_circulant', 0),
        'Trésorerie': data.get('tresorerie', 0)
    }
    
    # Passif
    passif_data = {
        'Capitaux Propres': data.get('capitaux_propres', 0),
        'Dettes Financières': data.get('dettes_financieres', 0),
        'Dettes Court Terme': data.get('dettes_court_terme', 0),
        'Trésorerie Passif': data.get('tresorerie_passif', 0)
    }
    
    # Créer deux sous-graphiques
    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'pie'}, {'type': 'pie'}]],
        subplot_titles=('Structure de l\'Actif', 'Structure du Passif')
    )
    
    # Graphique actif
    fig.add_trace(go.Pie(
        labels=list(actif_data.keys()),
        values=list(actif_data.values()),
        name="Actif",
        marker_colors=['#ff9999', '#66b3ff', '#99ff99']
    ), row=1, col=1)
    
    # Graphique passif
    fig.add_trace(go.Pie(
        labels=list(passif_data.keys()),
        values=list(passif_data.values()),
        name="Passif",
        marker_colors=['#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6']
    ), row=1, col=2)
    
    fig.update_layout(
        title="Structure Financière du Bilan",
        height=500
    )
    
    return fig

def create_trend_chart(historical_data):
    """Crée un graphique de tendance (pour données historiques futures)"""
    # Placeholder pour évolution temporelle
    fig = go.Figure()
    
    periods = list(historical_data.keys()) if historical_data else ['N-2', 'N-1', 'N']
    
    # Exemple avec quelques ratios clés
    metrics = {
        'ROE': [12, 14, 15],
        'Liquidité': [1.3, 1.5, 1.8],
        'Marge Nette': [3.2, 3.8, 4.2]
    }
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    for i, (metric, values) in enumerate(metrics.items()):
        fig.add_trace(go.Scatter(
            x=periods,
            y=values,
            mode='lines+markers',
            name=metric,
            line=dict(color=colors[i], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Évolution des Ratios Clés",
        xaxis_title="Période",
        yaxis_title="Valeur",
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_score_gauge(score):
    """Crée une jauge pour le score global"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Score Global BCEAO"},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "yellow"},
                {'range': [50, 75], 'color': "orange"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=400)
    return fig