import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __():
    # Email: 23f3002461@ds.study.iitm.ac.in
    # This notebook demonstrates reactive data analysis with Marimo
    # Cell 1: Import libraries and setup
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell
def __(mo):
    # Cell 2: Interactive Controls
    # Create slider to control sample size - this will trigger updates in dependent cells
    sample_size_slider = mo.ui.slider(
        start=10,
        stop=200,
        value=50,
        step=10,
        label="Sample Size"
    )
    
    # Create slider to control noise level
    noise_slider = mo.ui.slider(
        start=0.1,
        stop=2.0,
        value=0.5,
        step=0.1,
        label="Noise Level"
    )
    
    mo.md(f"""
    ## Interactive Data Analysis Dashboard
    
    Adjust the parameters below to see how they affect the linear relationship:
    
    {sample_size_slider}
    
    {noise_slider}
    """)
    return noise_slider, sample_size_slider


@app.cell
def __(noise_slider, np, sample_size_slider):
    # Cell 3: Generate Data (depends on Cell 2)
    # This cell automatically re-runs when slider values change
    # Data flow: sample_size_slider.value and noise_slider.value -> x, y, correlation
    
    n = sample_size_slider.value
    noise_level = noise_slider.value
    
    # Generate synthetic data with linear relationship plus noise
    np.random.seed(42)
    x = np.linspace(0, 10, n)
    y = 2.5 * x + 5 + np.random.normal(0, noise_level, n)
    
    # Calculate correlation coefficient
    correlation = np.corrcoef(x, y)[0, 1]
    
    return correlation, n, noise_level, x, y


@app.cell
def __(correlation, mo, n, noise_level, plt, x, y):
    # Cell 4: Visualization and Analysis (depends on Cell 3)
    # This cell automatically updates when data changes
    # Data flow: x, y, correlation, n, noise_level -> plot and markdown output
    
    # Create scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(x, y, alpha=0.6, s=50)
    
    # Add trend line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), "r--", linewidth=2, label=f"y = {z[0]:.2f}x + {z[1]:.2f}")
    
    ax.set_xlabel("X Variable", fontsize=12)
    ax.set_ylabel("Y Variable", fontsize=12)
    ax.set_title("Linear Relationship Analysis", fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Determine correlation strength
    if abs(correlation) > 0.8:
        strength = "strong"
        emoji = "🟢" * 5
    elif abs(correlation) > 0.5:
        strength = "moderate"
        emoji = "🟡" * 3
    else:
        strength = "weak"
        emoji = "🔴" * 2
    
    # Dynamic markdown output based on current state
    mo.md(f"""
    ### Analysis Results
    
    **Dataset Parameters:**
    - Sample Size: **{n}** observations
    - Noise Level: **{noise_level:.1f}**
    
    **Statistical Summary:**
    - Correlation Coefficient: **{correlation:.3f}**
    - Relationship Strength: **{strength}** {emoji}
    - Linear Model: y = {z[0]:.2f}x + {z[1]:.2f}
    
    **Interpretation:**
    The data shows a **{strength}** linear relationship between X and Y variables.
    {'Higher correlation indicates better predictive power!' if abs(correlation) > 0.8 else 'Try reducing noise to see a stronger pattern!'}
    
    {mo.as_html(fig)}
    """)
    return ax, emoji, fig, p, strength, z


@app.cell
def __(mo):
    # Cell 5: Documentation and Instructions
    mo.md("""
    ---
    ### How This Notebook Works
    
    This notebook demonstrates **reactive programming** in Marimo:
    
    1. **Cell 1**: Imports required libraries
    2. **Cell 2**: Creates interactive sliders (independent)
    3. **Cell 3**: Generates data based on slider values (depends on Cell 2)
    4. **Cell 4**: Creates visualization and analysis (depends on Cell 3)
    5. **Cell 5**: Static documentation (independent)
    
    **Try it out:** Move the sliders above and watch how the entire analysis updates automatically!
    
    The dependency graph ensures reproducibility - cells always execute in the correct order.
    """)
    return


if __name__ == "__main__":
    app.run()
