import { useSchedulingStore } from "@/store/useSchedulingStore";
import { Button } from "@/components/ui/button";

// Lista de serviços simulada (isso pode vir do backend depois)
const services = [
  { id: "corte", name: "Corte de Cabelo", price: "R$ 40,00" },
  { id: "barba", name: "Barba", price: "R$ 30,00" },
  { id: "combo", name: "Corte + Barba", price: "R$ 60,00" },
  { id: "sobrancelha", name: "Sobrancelha", price: "R$ 15,00" },
];

export function ServiceSelection() {
  const { selectedService, setSelectedService } = useSchedulingStore();

  return (
    <div className="grid grid-cols-2 gap-3">
      {services.map((service) => (
        <Button
          key={service.id}
          variant={selectedService === service.name ? "default" : "outline"}
          className="h-auto flex flex-col items-start p-4 text-left transition-all"
          onClick={() => setSelectedService(service.name)}
        >
          <span className="font-semibold">{service.name}</span>
          <span className="text-sm opacity-70 mt-1">{service.price}</span>
        </Button>
      ))}
    </div>
  );
}