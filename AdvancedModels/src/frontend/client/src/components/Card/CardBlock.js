import React from "react";
import { Card, CardHeader, CardContent, IconButton } from "@mui/material";
import { DeleteOutlined } from "@mui/icons-material/";

function CardBlock({ card }) {
    return (
        <div>
            <Card sx={{ margin:0.5 }}>
                <CardHeader
                    action={ 
                        <IconButton>
                            <DeleteOutlined />
                        </IconButton>
                    }
                    title={card.title}
                    subheader={card.category}
                />
            </Card>
        </div>
    );
}

export default CardBlock;
