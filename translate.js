const translate = require('google-translate-extended-api');

// Set default options for translation
const defaultDataOptions = {
    returnRawResponse: false,
    detailedTranslations: true,
    definitionSynonyms: false,
    detailedTranslationsSynonyms: false,
    definitions: true,
    definitionExamples: false,
    examples: true,
    removeStyles: true
};

// Enable definition synonyms and examples
translate.defaultDataOptions.definitionSynonyms = true;
translate.defaultDataOptions.definitionExamples = true;
translate.defaultDataOptions.detailedTranslationsSynonyms = true;

async function runTranslate(word, language, target) {
    try {
        const res = await translate(word, language, target);
        console.log(JSON.stringify(res, undefined, 2));
    } catch (error) {
        console.error("Translation error:", error);
    }
}

// Fetch command line arguments
const args = process.argv.slice(2);

// Check if enough arguments are provided
if (args.length !== 3) {
    console.error("Usage: node translate.js <word> <source_language> <target_language>");
    process.exit(1);
}

// Extract arguments
const [word, language, target] = args;

// Run translation
runTranslate(word, language, target);
