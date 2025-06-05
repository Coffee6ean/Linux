import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type FormField = {
    id: string;
    label: string;
    type?: string;
    placehdolder?: string;
    required?: boolean;
}

type DynamicFromProps = {
    fields: FormField[];
    values: Record<string, string>;
    errors?: Record<string, string>;
    onChange: (id:string, value:string) => void;
    onSubmit: () => void;
    submitText?: string;
    onCancel?: () => void;
    isLoading?: boolean;
};

export function DynamicForm({
    fields, 
    values, 
    errors={}, 
    onChange, 
    onSubmit, 
    submitText = "Submit", 
    onCancel, 
    isLoading = false}: DynamicFromProps) {
        return (
            <Card className="">
                <div className="">
                    <div className="">
                        {fields.map((field) => (
                            <div key={field.id}>
                                <Label htmlFor={field.id}>
                                    {field.label}
                                    {field.required && <span className="text-red-500">*</span>}
                                </Label>
                                <Input
                                    id={field.id}
                                    type={field.type || "text"}
                                    value={values[field.id] || ""}
                                    onChange={(e) => onChange(field.id, e.target.value)}
                                    placehdolder={field.placehdolder}
                                    error={errors[field.id]}
                                />
                            </div>
                        ))}
                    </div>

                    <div>
                        {onCancel && (
                            <Button 
                                type="button" 
                                variant="outline" 
                                onClick={onCancel} 
                                disabled={isLoading}
                            >
                                Cancel
                            </Button>
                        )}
                        <Button
                            type="button"
                            onClick={onSubmit}
                            disabled={isLoading}
                            isLoading={isLoading}
                        >
                            {submitText}
                        </Button>
                    </div>
                </div>
            </Card>
        )
    }
