# Healthy Recipe Generation: Fine-Tuned RecipeNLG

This repository contains our work on **fine-tuning a GPT-2 model using the RecipeNLG dataset and model** (INLG 2020) to generate recipes with a focus on low glycemic index (GI) ingredients. Our project builds on the original RecipeNLG resources, applying additional filtering and training to create a health-oriented recipe generator.

---

## 📦 Resources

- **Original data & code:**  
  RecipeNLG dataset and baseline models are available at [recipenlg.cs.put.poznan.pl](https://recipenlg.cs.put.poznan.pl/)
- **Reference paper:**  
  “RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation” (INLG 2020)  
  🔗 https://www.aclweb.org/anthology/2020.inlg-1.4.pdf

---

## 🌱 Healthy-Only Fine-Tuned Model

We filtered the original corpus to keep only recipes whose ingredients are known and predominantly low GI. Here’s how:

1. **Glycemic Index Lookup**  
  • Used the glycemic index chart from [foodstruct.com](https://foodstruct.com/glycemic-index-chart).  
    • Excluded ingredients with GI = 0 or missing.

2. **Filtering Recipes**  
   • Extracted ingredient names via NER.  
   • Kept recipes where all ingredients have known GI > 0 **and** ≥ 50 % of them have GI < 55.  
   • Saved as `dataset/h_recipes_50pct.csv`.

3. **Tokenization & Tags**  
   • Wrapped each recipe as

   ```
   <RECIPE_START>
   <INPUT_START>…<INPUT_END>
   <INGR_START>…<INGR_END>
   <INSTR_START>…<INSTR_END>
   <TITLE_START>…<TITLE_END>
   <RECIPE_END>
   ```

   • Items separated by `<NEXT_INPUT>`, `<NEXT_INGR>`, `<NEXT_INSTR>`.  
   • File: `dataset/h_recipes_50pct_token.csv`.

4. **Length Filtering**  
   • Removed any recipe over 400 tokens (to speed up training).  
   • Final: `dataset/h_recipes_50pct_token_max400.csv`.

---

## ⚙️ Prompt & Generation Parameters

Below is the **exact prompt** and parameter set we used when generating recipes.

```text
Give me a healthy recipe using the following ingredients (you don't have to use all of them):
<RECIPE_START>
<INPUT_START>chocolate<NEXT_INPUT>pickles<NEXT_INPUT>beef<NEXT_INPUT>pear<INPUT_END>
```

### Training Hyperparameters

When fine-tuning, we used (inspired by pratultandon/recipe-nlg-gpt2):

- **Learning rate**: 5e-5
- **Batch size**: 8 (per device for train & eval)
- **Epochs**: 1 (start with 1; increase to 2–3 if loss has not plateaued)
- **Optimizer**: AdamW (betas=(0.9,0.999), eps=1e-8)
- **Scheduler**: Linear with `warmup_steps=50`
- **Mixed precision**: `fp16=True` on GPU (as Google Colab was used)
- **Seed**: 42

See `retrain.ipynb` for the full training script.

### Tokenization

- **truncation**=True
- **max_length**=512
- **return_attention_mask**=True

### Generation

- **max_length**=512
- **num_beams**=2 (or 5)
- **no_repeat_ngram_size**=2
- **early_stopping**=True
- **eos_token_id** = ID of <RECIPE_END>

---

## Attribution & Citations

- **Original Dataset/Model**:
  _RecipeNLG: A Cooking Recipes Dataset for Semi-Structured Text Generation_, INLG 2020.