/**
 * Hashing utilities for event IDs and file checksums
 */

import * as crypto from 'crypto';
import * as fs from 'fs';
import { v4 as uuidv4 } from 'uuid';

export function generateEventId(source: string, recordId: string, timestamp: string): string {
  const input = `${source}:${recordId}:${timestamp}`;
  return crypto.createHash('sha256').update(input).digest('hex').substring(0, 16);
}

export function generatePointerId(type: string, value: string): string {
  const input = `${type}:${value}`;
  return `ptr_${crypto.createHash('sha256').update(input).digest('hex').substring(0, 12)}`;
}

export function generateRunId(): string {
  return `run_${uuidv4().replace(/-/g, '').substring(0, 16)}`;
}

export function generateClusterId(): string {
  return `cluster_${uuidv4().replace(/-/g, '').substring(0, 12)}`;
}

export function hashString(input: string): string {
  return crypto.createHash('sha256').update(input).digest('hex');
}

export async function hashFile(filePath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const stream = fs.createReadStream(filePath);

    stream.on('data', (data) => hash.update(data));
    stream.on('end', () => resolve(hash.digest('hex')));
    stream.on('error', (err) => reject(err));
  });
}

export function hashFileSync(filePath: string): string {
  const content = fs.readFileSync(filePath);
  return crypto.createHash('sha256').update(content).digest('hex');
}

export function generateChecksum(data: object): string {
  const json = JSON.stringify(data, null, 0);
  return crypto.createHash('sha256').update(json).digest('hex');
}
