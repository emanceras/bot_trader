import type { ComponentType } from 'react';
import { Overview, Hypotheses, Datasets, Experiments, Modules, Audit } from './views';
import type { Session } from './types';

export type SectionId = 'overview' | 'hypotheses' | 'datasets' | 'experiments' | 'modules' | 'audit';
export interface Section {
  id: SectionId;
  label: string;
  title: string;
  kicker: string;
  description: string;
  symbol: string;
  component: ComponentType<{ session: Session }>;
}

/** Navigation metadata is independent of domain services and chart rendering. */
export const sections: readonly Section[] = [
  { id: 'overview', label: 'Vista general', title: 'Una base para investigar.', kicker: 'EL LABORATORIO', description: 'Estado de la plataforma y trazabilidad del trabajo de investigación.', symbol: '◈', component: Overview },
  { id: 'hypotheses', label: 'Hipótesis', title: 'Preguntas antes que resultados.', kicker: 'REGISTRO CIENTÍFICO', description: 'Hipótesis originales, sus nulas y condiciones de refutación. Ninguna está validada financieramente.', symbol: '◇', component: Hypotheses },
  { id: 'datasets', label: 'Datos y gráficos', title: 'Cada dato tiene un origen.', kicker: 'CATÁLOGO DE DATOS', description: 'Fixtures sintéticas, versiones inmutables y series con disponibilidad temporal explícita.', symbol: '▥', component: Datasets },
  { id: 'experiments', label: 'Pruebas técnicas', title: 'Ejecuciones que dejan rastro.', kicker: 'LABORATORIO TÉCNICO', description: 'Configuración, entorno, estados, resultados y fallos persistidos en cada intento.', symbol: '⌁', component: Experiments },
  { id: 'modules', label: 'Módulos', title: 'Una plataforma que evoluciona.', kicker: 'ARQUITECTURA MODULAR', description: 'Capacidades declaradas por el backend, dependencias y estado de implementación.', symbol: '▦', component: Modules },
  { id: 'audit', label: 'Actividad y errores', title: 'Lo que ocurrió, registrado.', kicker: 'OBSERVABILIDAD', description: 'Acciones, fallos y referencias para inspeccionar el funcionamiento de la plataforma.', symbol: '≡', component: Audit },
];
