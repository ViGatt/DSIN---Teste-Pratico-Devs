import * as React from "react";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { useSchedulingStore } from "@/store/useSchedulingStore";

export function DatePicker() {
  const { selectedDate, setSelectedDate } = useSchedulingStore();

  return (
    <Popover>
      {/* @ts-expect-error: Silenciando falso positivo de tipagem em cache do Base UI */}
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "w-full justify-start text-left font-normal",
            !selectedDate && "text-muted-foreground"
          )}
        >
          <CalendarIcon className="mr-2 h-4 w-4" />
          {selectedDate ? format(selectedDate, "PPP") : <span>Selecione uma data</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          selected={selectedDate || undefined}
          onSelect={(date) => setSelectedDate(date ?? null)}
          required={false}
        />
      </PopoverContent>
    </Popover>
  );
}