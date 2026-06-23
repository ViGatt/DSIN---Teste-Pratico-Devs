import DatePicker, { registerLocale } from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { ptBR } from 'date-fns/locale/pt-BR';
import { setHours, setMinutes, getDay } from "date-fns"; // Importe estas funções

registerLocale('pt-BR', ptBR);

interface Props {
  selectedDate: Date | null;
  onChange: (date: Date | null) => void;
}

export function DatePickerCustom({ selectedDate, onChange }: Props) {
  
  // Função para desabilitar Domingos (dia 0)
  const isNotSunday = (date: Date) => {
    const day = getDay(date);
    return day !== 0; 
  };

  return (
    <div className="w-full">
      <DatePicker
        selected={selectedDate}
        onChange={onChange}
        showTimeSelect
        shouldCloseOnSelect={true} // Fecha automaticamente após selecionar a hora
        locale="pt-BR"
        dateFormat="dd/MM/yyyy HH:mm"
        
        // Trava de horário: das 08:00 às 17:00
        minTime={setHours(setMinutes(new Date(), 0), 8)}
        maxTime={setHours(setMinutes(new Date(), 0), 17)}
        
        // Filtro para bloquear domingos
        filterDate={isNotSunday}
        
        placeholderText="Selecione data e hora"
        className="flex h-12 w-full rounded-lg border border-zinc-300 bg-white px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
        wrapperClassName="w-full"
        calendarClassName="shadow-2xl border border-zinc-200 rounded-xl p-2"
      />
    </div>
  );
}