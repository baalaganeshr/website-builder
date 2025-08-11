// Keep in sync with backend - Updated with exact model names
// Order here matches dropdown order
export enum CodeGenerationModel {
  GPT_OSS_20B = "gpt-oss-20b",
  LLAMA3_2_3B = "llama3.2:3b",
}

// Will generate a static error if a model in the enum above is not in the descriptions
export const CODE_GENERATION_MODEL_DESCRIPTIONS: {
  [key in CodeGenerationModel]: { name: string; inBeta: boolean };
} = {
  "gpt-oss-20b": { name: "GPT OSS 20B (Large Model)", inBeta: false },
  "llama3.2:3b": { name: "Llama 3.2 3B (Fast)", inBeta: false },
};
