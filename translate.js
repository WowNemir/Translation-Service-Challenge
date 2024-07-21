const translate = require('google-translate-extended-api');

// default options are here as documentation
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

const args = process.argv.slice(2);

if (args.length !== 3) {
    console.error("Usage: node translate.js <word> <source_language> <target_language>");
    process.exit(1);
}

const [word, language, target] = args;

runTranslate(word, language, target);
