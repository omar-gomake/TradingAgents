# Phase 5: Ensemble Prediction with FinGPT
## Combine Multiple LLM Models for Superior Forecasting

**Duration:** 2 weeks (Weeks 9-10)
**Difficulty:** Medium
**Impact:** ⭐⭐⭐⭐ (+10-15% from model diversity)
**Prerequisites:** Phases 1-2 completed

---

## Overview

Combine predictions from multiple LLM models to reduce model-specific biases and improve accuracy:

- **GPT-4o**: General reasoning
- **o4-mini**: Deep analytical thinking
- **Claude 3.5**: Alternative perspective
- **FinGPT-Forecaster**: Domain-specific financial prediction

**Key Insight:** When models disagree significantly, uncertainty is high → reduce position size or wait.

---

## Architecture

```python
# tradingagents/agents/predictors/ensemble_predictor.py

class EnsemblePredictor:
    """Combine predictions from multiple LLM models."""

    def __init__(self):
        self.models = {
            'gpt4o': ChatOpenAI(model="gpt-4o"),
            'o4mini': ChatOpenAI(model="o4-mini"),
            'claude': ChatAnthropic(model="claude-3-5-sonnet-20241022"),
            'fingpt': self._init_fingpt()  # FinGPT integration
        }

    def predict(
        self,
        ticker: str,
        analyst_reports: Dict[str, str],
        horizon: str = "2_weeks"
    ) -> Dict[str, Any]:
        """
        Get ensemble prediction from all models.

        Returns:
            {
                'predicted_return': 0.12,  # Weighted average
                'confidence_interval': (0.05, 0.20),
                'uncertainty': 0.35,  # Model disagreement
                'model_predictions': {
                    'gpt4o': 0.15,
                    'o4mini': 0.11,
                    'claude': 0.10,
                    'fingpt': 0.13
                },
                'recommendation': 'BUY',
                'position_size_multiplier': 0.8  # Reduce if high uncertainty
            }
        """
        predictions = {}

        # Get prediction from each model
        for model_name, model in self.models.items():
            pred = self._get_single_prediction(
                model, ticker, analyst_reports, horizon
            )
            predictions[model_name] = pred

        # Calculate ensemble metrics
        mean_pred = np.mean(list(predictions.values()))
        std_pred = np.std(list(predictions.values()))
        uncertainty = std_pred / abs(mean_pred) if mean_pred != 0 else 1.0

        # Adjust position size based on uncertainty
        if uncertainty < 0.2:
            position_multiplier = 1.0  # High confidence
        elif uncertainty < 0.4:
            position_multiplier = 0.7  # Medium confidence
        else:
            position_multiplier = 0.4  # Low confidence

        return {
            'predicted_return': mean_pred,
            'confidence_interval': (mean_pred - 2*std_pred, mean_pred + 2*std_pred),
            'uncertainty': uncertainty,
            'model_predictions': predictions,
            'position_size_multiplier': position_multiplier
        }

    def _get_single_prediction(
        self,
        model,
        ticker: str,
        analyst_reports: Dict,
        horizon: str
    ) -> float:
        """Get prediction from single model."""
        prompt = f"""
        Based on the following analyst reports, predict the expected return
        for {ticker} over the next {horizon}.

        {analyst_reports}

        Provide ONLY a number representing expected return as a decimal
        (e.g., 0.15 for 15% gain, -0.05 for 5% loss).
        """

        response = model.invoke(prompt)
        # Parse number from response
        return self._parse_return_prediction(response.content)
```

---

## Model Weighting

Track each model's accuracy and weight by performance:

```python
# tradingagents/agents/predictors/model_tracker.py

class ModelPerformanceTracker:
    """Track prediction accuracy by model."""

    def record_prediction_outcome(
        self,
        model_name: str,
        prediction: float,
        actual_return: float,
        regime: str
    ):
        """Record for learning which models are best in which regimes."""
        pass

    def get_model_weights(self, regime: str) -> Dict[str, float]:
        """
        Return performance-based weights.

        Example:
            {
                'gpt4o': 0.30,
                'o4mini': 0.35,  # Best performer
                'claude': 0.25,
                'fingpt': 0.10  # Worst performer
            }
        """
        pass
```

---

## Expected Results

- **Reduced overfitting** to any single model's biases
- **Better uncertainty quantification** via model disagreement
- **Adaptive position sizing** based on prediction confidence
- **+10-15% improvement** in risk-adjusted returns

---

## Next Phase

Continue to [08_PHASE6_AUTONOMOUS_PORTFOLIO.md](08_PHASE6_AUTONOMOUS_PORTFOLIO.md)
