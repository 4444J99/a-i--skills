#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const https = require('https');

/**
 * Creates a hash from input string
 * Takes first 16 characters of SHA256 hash and formats as xxxx-xxxx-xxxx-xxxx
 */
function createHash(input) {
    const fullHash = crypto.createHash('sha256').update(input).digest('hex');
    const truncatedHash = fullHash.substring(0, 16);
    return truncatedHash.replace(/(.{4})(.{4})(.{4})(.{4})/, '$1-$2-$3-$4');
}

/**
 * Gets the repo name from .git/config file
 */
function getRepoNameFromGitConfig() {
    const gitConfigPath = path.join(process.cwd(), '.git', 'config');

    if (!fs.existsSync(gitConfigPath)) {
        return null;
    }

    try {
        const configContent = fs.readFileSync(gitConfigPath, 'utf8');
        const lines = configContent.split('\n');

        let inOriginSection = false;
        for (const line of lines) {
            if (line.trim() === '[remote "origin"]') {
                inOriginSection = true;
                continue;
            }

            if (inOriginSection && line.includes('url =')) {
                const url = line.split('url =')[1].trim();
                // Extract repo name from URL
                // Handles both SSH (git@github.com:user/repo.git) and HTTPS (https://github.com/user/repo.git)
                const match = url.match(/[\/:]([^\/]+\/[^\/]+?)(\.git)?$/);
                if (match) {
                    return match[1].replace('.git', '');
                }
            }

            // Stop when we hit the next section
            if (inOriginSection && line.trim().startsWith('[')) {
                break;
            }
        }
    } catch (error) {
        console.error('Error reading .git/config:', error.message);
    }

    return null;
}

/**
 * Gets the current folder name
 */
function getCurrentFolderName() {
    return path.basename(process.cwd());
}

/**
 * Calculates the project ID
 */
function calculateProjectId() {
    // First, check if .specstory/.project.json exists
    const projectJsonPath = path.join(process.cwd(), '.specstory', '.project.json');

    if (fs.existsSync(projectJsonPath)) {
        try {
            const projectData = JSON.parse(fs.readFileSync(projectJsonPath, 'utf8'));

            // Prefer git_id, fallback to workspace_id
            if (projectData.git_id) {
                return projectData.git_id;
            }
            if (projectData.workspace_id) {
                return projectData.workspace_id;
            }
        } catch (error) {
            console.error('Error reading .specstory/.project.json:', error.message);
        }
    }

    // Calculate from repo name or folder name
    const repoName = getRepoNameFromGitConfig();
    const identifier = repoName || getCurrentFolderName();

    return createHash(identifier);
}

/**
 * Fetches stats from the API
 */
function fetchStats(projectId, baseUrl) {
    const url = `${baseUrl}/api/v1/projects/${projectId}/stats`;
    const urlObj = new URL(url);
    const isHttps = urlObj.protocol === 'https:';
    const http = require('http');
    const httpModule = isHttps ? https : http;

    return new Promise((resolve, reject) => {
        httpModule.get(url, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                if (res.statusCode === 200) {
                    try {
                        const jsonData = JSON.parse(data);
                        resolve(jsonData);
                    } catch (error) {
                        reject(new Error(`Failed to parse JSON response: ${error.message}`));
                    }
                } else {
                    reject(new Error(`API returned status ${res.statusCode}: ${data}`));
                }
            });
        }).on('error', (error) => {
            reject(new Error(`Request failed: ${error.message}`));
        });
    });
}

/**
 * Main function
 */
async function main() {
    try {
        const baseUrl = process.env.SPECSTORY_API_URL || 'https://cloud.specstory.com';
        const projectId = calculateProjectId();

        console.log(`Project ID: ${projectId}`);
        console.log(`Fetching stats from: ${baseUrl}/api/v1/projects/${projectId}/stats\n`);

        const stats = await fetchStats(projectId, baseUrl);

        console.log('Stats:');
        console.log(JSON.stringify(stats, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

main();
