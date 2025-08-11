// Keep in sync with backend (llm.py)
// Order here matches dropdown order
export enum CodeGenerationModel {
  OLLAMA_GPT_LOCAL = "llama3.2:latest",
}

// Will generate a static error if a model in the enum above is not in the descriptions
export const CODE_GENERATION_MODEL_DESCRIPTIONS: {
  [key in CodeGenerationModel]: { name: string; inBeta: boolean };
} = {
  "llama3.2:latest": { name: "Local Llama 3.2 3B (Private)", inBeta: false },
};
