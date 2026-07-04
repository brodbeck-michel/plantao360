/**
 * Frontend Validator — Plantão 360
 *
 * Valida estrutura, imports, API contracts e naming de features.
 *
 * Sprint: 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
 */

import * as fs from 'fs';
import * as path from 'path';

// ============================================================
// Types
// ============================================================

interface ValidationResult {
  feature: string;
  passed: boolean;
  errors: string[];
  warnings: string[];
}

interface ManifestData {
  name: string;
  golden_module?: boolean;
  routes: Record<string, {
    path: string | string[];
    component: string;
    personas: string[];
    endpoints: string[];
  }>;
  components: string[];
  hooks: string[];
  services: string[];
  types: string[];
}

// ============================================================
// Constants
// ============================================================

const FORBIDDEN_IMPORTS = [
  'axios',
  'src/api/client',
  'src/config/api',
  'src/config/urls',
];

const REQUIRED_STRUCTURE = {
  directories: ['components', 'hooks', 'services', 'types', 'pages'],
  files: ['index.ts'],
};

const FEATURE_BASE_PATH = path.resolve(__dirname, '../features');
const MANIFESTS_PATH = path.resolve(__dirname, '../../manifests');

// ============================================================
// Validators
// ============================================================

function validateStructure(featureName: string): ValidationResult {
  const featurePath = path.join(FEATURE_BASE_PATH, featureName);
  const errors: string[] = [];
  const warnings: string[] = [];

  // Check required directories
  for (const dir of REQUIRED_STRUCTURE.directories) {
    const dirPath = path.join(featurePath, dir);
    if (!fs.existsSync(dirPath)) {
      errors.push(`Missing required directory: ${dir}`);
    }
  }

  // Check required files
  for (const file of REQUIRED_STRUCTURE.files) {
    const filePath = path.join(featurePath, file);
    if (!fs.existsSync(filePath)) {
      warnings.push(`Missing recommended file: ${file}`);
    }
  }

  return {
    feature: featureName,
    passed: errors.length === 0,
    errors,
    warnings,
  };
}

function validateImports(featureName: string): ValidationResult {
  const featurePath = path.join(FEATURE_BASE_PATH, featureName);
  const errors: string[] = [];
  const warnings: string[] = [];

  function checkFile(filePath: string) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      for (const forbidden of FORBIDDEN_IMPORTS) {
        if (line.includes(forbidden)) {
          errors.push(
            `Forbidden import in ${path.relative(featurePath, filePath)}:${i + 1}: ${forbidden}`
          );
        }
      }
    }
  }

  function walkDir(dir: string) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);
      if (stat.isDirectory()) {
        walkDir(filePath);
      } else if (file.endsWith('.ts') || file.endsWith('.tsx')) {
        checkFile(filePath);
      }
    }
  }

  walkDir(featurePath);

  return {
    feature: featureName,
    passed: errors.length === 0,
    errors,
    warnings,
  };
}

function validateManifest(featureName: string): ValidationResult {
  const manifestPath = path.join(MANIFESTS_PATH, `${featureName}.json`);
  const errors: string[] = [];
  const warnings: string[] = [];

  if (!fs.existsSync(manifestPath)) {
    errors.push(`Manifest file not found: ${featureName}.json`);
    return {
      feature: featureName,
      passed: false,
      errors,
      warnings,
    };
  }

  const manifest: ManifestData = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));

  // Validate manifest structure
  if (!manifest.name) {
    errors.push('Manifest missing "name" field');
  }
  if (!manifest.routes || Object.keys(manifest.routes).length === 0) {
    errors.push('Manifest missing "routes" field');
  }
  if (!manifest.components || manifest.components.length === 0) {
    warnings.push('Manifest has no components listed');
  }

  // Validate endpoints are absolute paths
  if (manifest.routes) {
    for (const [routeName, route] of Object.entries(manifest.routes)) {
      if (route.endpoints) {
        for (const endpoint of route.endpoints) {
          if (!endpoint.startsWith('GET ') &&
              !endpoint.startsWith('POST ') &&
              !endpoint.startsWith('PUT ') &&
              !endpoint.startsWith('DELETE ') &&
              !endpoint.startsWith('PATCH ')) {
            errors.push(`Route "${routeName}" has invalid endpoint format: ${endpoint}`);
          }
        }
      }
    }
  }

  return {
    feature: featureName,
    passed: errors.length === 0,
    errors,
    warnings,
  };
}

function validateNaming(featureName: string): ValidationResult {
  const errors: string[] = [];
  const warnings: string[] = [];

  // Feature name must be kebab-case
  if (!/^[a-z][a-z0-9]*(-[a-z0-9]+)*$/.test(featureName)) {
    errors.push(`Feature name "${featureName}" must be kebab-case`);
  }

  return {
    feature: featureName,
    passed: errors.length === 0,
    errors,
    warnings,
  };
}

// ============================================================
// Main Validator
// ============================================================

export function validateFeature(featureName: string): ValidationResult[] {
  const results: ValidationResult[] = [];

  results.push(validateNaming(featureName));
  results.push(validateStructure(featureName));
  results.push(validateImports(featureName));
  results.push(validateManifest(featureName));

  return results;
}

export function validateAllFeatures(): ValidationResult[] {
  const results: ValidationResult[] = [];
  const features = fs.readdirSync(FEATURE_BASE_PATH);

  for (const feature of features) {
    const featurePath = path.join(FEATURE_BASE_PATH, feature);
    if (fs.statSync(featurePath).isDirectory()) {
      results.push(...validateFeature(feature));
    }
  }

  return results;
}

// ============================================================
// CLI Runner
// ============================================================

if (require.main === module) {
  const featureName = process.argv[2];
  let results: ValidationResult[];

  if (featureName) {
    console.log(`\n🔍 Validating feature: ${featureName}\n`);
    results = validateFeature(featureName);
  } else {
    console.log('\n🔍 Validating all features...\n');
    results = validateAllFeatures();
  }

  const allPassed = results.every((r) => r.passed);

  for (const result of results) {
    const icon = result.passed ? '✅' : '❌';
    console.log(`${icon} ${result.feature}:`);

    for (const error of result.errors) {
      console.log(`   ❌ ${error}`);
    }

    for (const warning of result.warnings) {
      console.log(`   ⚠️  ${warning}`);
    }

    if (result.errors.length === 0 && result.warnings.length === 0) {
      console.log('   All checks passed');
    }

    console.log('');
  }

  console.log(allPassed ? '\n✅ All validations passed\n' : '\n❌ Some validations failed\n');
  process.exit(allPassed ? 0 : 1);
}
