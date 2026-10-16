import { promises as fs } from 'node:fs';
import path from 'node:path';

export interface Linea {
  numero: string;
  nombre: string;
  esEjemplo?: boolean;
  empresa: string;
  descripcionCorta?: string;
  recorrido?: {
    ida?: {
      descripcion: string;
      calles: string[];
    };
    vuelta?: {
      descripcion: string;
      calles: string[];
    };
  };
  paradasPrincipales?: string[];
  horarios?: {
    lunesAViernes?: {
      tipo: string;
      descripcion: string;
      horarioInicio: string;
      horarioFin: string;
    };
    sabados?: {
      tipo: string;
      descripcion: string;
      horarioInicio: string;
      horarioFin: string;
    };
    domingosYFeriados?: {
      tipo: string;
      descripcion: string;
      horarioInicio: string;
      horarioFin: string;
    };
  };
  tarifas?: {
    efectivo?: string;
    redBus?: string;
  };
  mapsEmbedUrl?: string;
  ultimaActualizacion?: string;
  fuente?: string;
  notas?: string;
}

let lineasCache: Linea[] | null = null;

export async function getLineas(): Promise<Linea[]> {
  if (lineasCache) {
    return lineasCache;
  }

  const lineasDir = path.join(process.cwd(), 'src/data/lineas');
  
  try {
    const files = await fs.readdir(lineasDir);
    const jsonFiles = files.filter(file => file.startsWith('linea-') && file.endsWith('.json'));
    
    const lineas = await Promise.all(
      jsonFiles.map(async (file) => {
        const filePath = path.join(lineasDir, file);
        const content = await fs.readFile(filePath, 'utf-8');
        return JSON.parse(content) as Linea;
      })
    );

    lineasCache = lineas.sort((a, b) => {
      const getNumericPart = (num: string) => {
        const match = num.match(/^(\d+)/);
        return match ? parseInt(match[1], 10) : 9999;
      };
      
      const numA = getNumericPart(a.numero);
      const numB = getNumericPart(b.numero);
      
      if (numA !== numB) {
        return numA - numB;
      }
      
      return a.numero.localeCompare(b.numero, undefined, { numeric: true });
    });

    return lineasCache;
  } catch (error) {
    console.error('Error loading lineas:', error);
    return [];
  }
}

export async function getLineaByNumero(numero: string): Promise<Linea | undefined> {
  const lineas = await getLineas();
  return lineas.find(linea => linea.numero === numero);
}

export function getRecorridoSummary(linea: Linea): string {
  if (!linea.recorrido) return 'Información de recorrido pendiente';
  
  const ida = linea.recorrido.ida?.descripcion;
  const vuelta = linea.recorrido.vuelta?.descripcion;
  
  if (ida && vuelta) {
    return `${ida} / ${vuelta}`;
  }
  
  if (ida) return ida;
  if (vuelta) return vuelta;
  
  return 'Información de recorrido pendiente';
}

export function hasValidSchedule(linea: Linea): boolean {
  if (!linea.horarios) return false;
  
  const weekday = linea.horarios.lunesAViernes;
  if (weekday && weekday.horarioInicio && weekday.horarioFin) {
    return true;
  }
  
  return false;
}
