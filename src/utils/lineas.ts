import fs from 'fs';
import path from 'path';
import type { LineaColectivo } from '../types';

const lineasDir = path.join(process.cwd(), 'src/data/lineas');

export function getAllLineas(): LineaColectivo[] {
  const files = fs.readdirSync(lineasDir).filter(file => file.endsWith('.json'));
  
  return files.map(file => {
    const content = fs.readFileSync(path.join(lineasDir, file), 'utf-8');
    return JSON.parse(content) as LineaColectivo;
  }).sort((a, b) => {
    const numA = parseInt(a.numero);
    const numB = parseInt(b.numero);
    return numA - numB;
  });
}

export function getLineaByNumero(numero: string): LineaColectivo | undefined {
  const lineas = getAllLineas();
  return lineas.find(linea => linea.numero === numero);
}
