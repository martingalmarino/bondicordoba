export interface Linea {
  numero: string;
  nombre?: string;
  recorrido?: string;
  empresa?: string;
  ida?: string;
  vuelta?: string;
  horarios?: Array<{
    dia: string;
    horario: string;
    frecuencia: string;
  }>;
  tarifas?: Array<{
    tipo: string;
    precio: number;
  }>;
  notas?: string[];
  fuente?: string;
}

const lineasData: Linea[] = [
  {
    numero: "1",
    nombre: "Villa Eucarística - Ferreyra",
    recorrido: "Villa Eucarística - Centro - Ferreyra",
    empresa: "Coniferal",
    ida: "Villa Eucarística, Recta Martinolli, Av. O'Higgins, Centro, Av. Colón, Circunvalación, Ferreyra",
    vuelta: "Ferreyra, Circunvalación, Av. Colón, Centro, Av. O'Higgins, Recta Martinolli, Villa Eucarística",
    fuente: "Empresa Coniferal"
  },
  {
    numero: "2",
    nombre: "Ciudad Universitaria - Argüello",
    recorrido: "Ciudad Universitaria - Centro - Argüello Norte",
    empresa: "Coniferal",
    ida: "Ciudad Universitaria, Av. Vélez Sarsfield, Centro, Av. Colón, Av. Recta Martinolli, Argüello Norte",
    vuelta: "Argüello Norte, Av. Recta Martinolli, Av. Colón, Centro, Av. Vélez Sarsfield, Ciudad Universitaria",
    fuente: "Empresa Coniferal"
  },
  {
    numero: "3",
    nombre: "Barrio Los Boulevares - Alta Córdoba",
    recorrido: "Barrio Los Boulevares - Centro - Alta Córdoba",
    empresa: "Coniferal",
    ida: "Barrio Los Boulevares, Av. Sabattini, Centro, Av. Colón, Barrio Alta Córdoba",
    vuelta: "Alta Córdoba, Av. Colón, Centro, Av. Sabattini, Barrio Los Boulevares",
    fuente: "Empresa Coniferal"
  },
  {
    numero: "10",
    nombre: "Villa Adela - Cerro Norte",
    recorrido: "Villa Adela - Centro - Cerro de las Rosas",
    empresa: "Ciudad de Córdoba",
    fuente: "Empresa Ciudad de Córdoba"
  },
  {
    numero: "20",
    nombre: "Alto Alberdi - Jardín",
    recorrido: "Alto Alberdi - Centro - Barrio Jardín",
    empresa: "ERSA",
    fuente: "Empresa ERSA"
  },
  {
    numero: "30",
    nombre: "San Vicente - Villa Belgrano",
    recorrido: "Barrio San Vicente - Centro - Villa Belgrano",
    empresa: "Ciudad de Córdoba",
    fuente: "Empresa Ciudad de Córdoba"
  }
];

export async function getLineas(): Promise<Linea[]> {
  return lineasData.sort((a, b) => {
    const numA = parseInt(a.numero, 10);
    const numB = parseInt(b.numero, 10);
    if (!isNaN(numA) && !isNaN(numB)) {
      return numA - numB;
    }
    return a.numero.localeCompare(b.numero);
  });
}

export async function getLineaByNumero(numero: string): Promise<Linea | undefined> {
  const lineas = await getLineas();
  return lineas.find(linea => linea.numero === numero);
}
