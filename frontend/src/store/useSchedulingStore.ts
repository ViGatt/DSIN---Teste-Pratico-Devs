import { create } from 'zustand';

interface SchedulingState {
  clientData: { name: string; phone: string } | null;
  selectedDate: Date | null;
  selectedService: string | null;
  setClientData: (data: { name: string; phone: string }) => void;
  setSelectedDate: (date: Date | null) => void;
  setSelectedService: (service: string) => void;
}

export const useSchedulingStore = create<SchedulingState>((set) => ({
  clientData: null,
  selectedDate: null,
  selectedService: null,
  setClientData: (data) => set({ clientData: data }),
  setSelectedDate: (date) => set({ selectedDate: date }),
  setSelectedService: (service) => set({ selectedService: service }),
}));