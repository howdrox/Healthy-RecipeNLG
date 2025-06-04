# RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation

Model accompanying our INLG 2020 paper: [RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation](https://www.aclweb.org/anthology/2020.inlg-1.4.pdf)

---

## Where is the dataset?

Please visit the website of our project: [recipenlg.cs.put.poznan.pl](https://recipenlg.cs.put.poznan.pl/) to download it.

---

## New: Healthy-Only Fine-Tuned Model

We have retrained (fine-tuned) the original RecipeNLG model to generate **only low–glycemic index (GI) “healthy” recipes**. Below are details on how we filtered, formatted, and retrained the model:

### 1. Preparing the Healthy Subset

1. **Glycemic Index Lookup**

   * We built a GI lookup table by combining public low/medium/high GI CSVs from [Daniellappv/Glucose‐Matters](https://github.com/Daniellappv/glucose-matters).
   * GI values of `0` or missing were treated as “no GI info” and those ingredients were excluded.

2. **Filtering Recipes**

   * Each recipe’s ingredients were extracted via NER.
   * A recipe was kept only if **all ingredients have a known GI > 0** and **≥ 50 % of those ingredients have GI < 55**.
   * The filtered set was saved as `dataset/h_recipes_50pct.csv`.

3. **Tokenization and Tags**

   * Every recipe was formatted into a single `<RECIPE_START>…<RECIPE_END>` string, with sections marked by:

     ```
     <INPUT_START>…<INPUT_END>       # ingredient names from NER
     <INGR_START>…<INGR_END>         # full ingredient lines
     <INSTR_START>…<INSTR_END>       # step-by-step directions
     <TITLE_START>…<TITLE_END>       # recipe title
     ```
   * Within each section, items were separated by `<NEXT_INPUT>`, `<NEXT_INGR>`, or `<NEXT_INSTR>` as appropriate.
   * The formatted file is `dataset/h_recipes_50pct_token.csv`.

4. **Token Length Filtering**

    * To increase training speed, recipes were further filtered to a maximum of 400 tokens.
    * Any recipe exceeding this limit was excluded from the final training set.
    * The filtered set was saved as `dataset/h_recipes_50pct_token_max400.csv"
---

## Training Hyperparameters

When fine-tuning, we used (inspired by pratultandon/recipe-nlg-gpt2):

* **Learning rate**: 5e-5
* **Batch size**: 8 (per device for train & eval)
* **Epochs**: 1 (start with 1; increase to 2–3 if loss has not plateaued)
* **Optimizer**: AdamW (betas=(0.9,0.999), eps=1e-8)
* **Scheduler**: Linear with `warmup_steps=50`
* **Mixed precision**: `fp16=True` on GPU (as Google Colab was used)
* **Seed**: 42
* **Save steps**: 50 (keep the latest 2 checkpoints)
* **Logging steps**: 100 (loss & lr to TensorBoard, no WandB)

See `notebooks/retrain.ipynb` (or `retrain_fixed.ipynb`) for the full training script.

---

## Attribution & Citations

* **Original Dataset/Model**:
  *RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation*, INLG 2020.
* **Our Fine-Tune**:
  We thank the original authors for providing the corpus. Our contribution is a “healthy‐oriented” fine‐tuned checkpoint available in `finetuned_recipenlg/`.

---

function stayAwake(){
  setInterval(() => {
    window.scrollBy(0, 1);
    window.scrollBy(0, -1);
  }, 60000);
}
stayAwake();