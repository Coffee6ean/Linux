import React, { useState } from "react";
import { Select, MenuItem } from "@mui/material";

function DropdownButton() {
    const options = [
        { value: 'default', label: 'Select Option' },
        { value: 'option1', label: 'Option 1' },
        { value: 'option2', label: 'Option 2' },
        { value: 'option3', label: 'Option 3' }
    ];

    const [selectedOption, setSelectedOption] = useState(options[0]);

    const handleChange = (event) => {
        const selectedValue = event.target.value;
        const option = options.find(opt => opt.value === selectedValue);
        setSelectedOption(option);
    };

    return (
        <div>
            <Select
                value={selectedOption.value}
                onChange={handleChange}
            >
                {options.map(option => (
                    <MenuItem key={option.value} value={option.value}>
                        {option.label}
                    </MenuItem>
                ))}
            </Select>
        </div>
    );
}

export default DropdownButton;
