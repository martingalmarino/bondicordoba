export interface Recorrido {
  descripcion: string;
  calles: string[];
}

export interface Horario {
  tipo: 'frecuencia' | 'horarios';
  descripcion: string;
  horarioInicio: string;
  horarioFin: string;
  horarios?: string[];
}

export interface LineaColectivo {
  numero: string;
  nombre: string;
  esEjemplo?: boolean;
  empresa: string;
  descripcionCorta: string;
  recorrido: {
    ida: Recorrido;
    vuelta: Recorrido;
  };
  paradasPrincipales: string[];
  horarios: {
    lunesAViernes: Horario;
    sabados: Horario;
    domingosYFeriados: Horario;
  };
  tarifas: {
    efectivo: string;
    redBus: string;
  };
  mapsEmbedUrl?: string;
  ultimaActualizacion: string;
  fuente: string;
  notas?: string;
}
