from typing import Any

class MWSGptForTest:
    async def generate_schema(self, message: str) -> dict[str, Any]:
        return (
            {
                "process_name": "Обработка заказа в интернет-магазине",
                "version": "1.2",
                "steps": {
                    "order_creation": {
                        "description": "Клиент создает заказ",
                        "sub_steps": [
                            {"action": "Выбор товаров", "required": True},
                            {"action": "Добавление в корзину", "required": True},
                            {"action": "Применение промокода", "required": False},
                        ],
                        "timeout_sec": 1800,
                    },
                    "payment": {
                        "description": "Оплата заказа",
                        "methods": ["credit_card", "paypal", "bank_transfer"],
                        "retry_count": 3,
                        "on_failure": {
                            "action": "notify_user",
                            "fallback_method": "cash_on_delivery",
                        },
                    },
                    "inventory_check": {
                        "description": "Проверка наличия товаров",
                        "auto": True,
                        "conditions": {
                            "in_stock": {"next_step": "packaging"},
                            "out_of_stock": {
                                "next_step": "notify_supplier",
                                "delay_days": 2,
                            },
                            "partial_stock": {
                                "next_step": "split_shipment",
                                "backorder": True,
                            },
                        },
                    },
                    "packaging": {
                        "description": "Упаковка заказа",
                        "materials": ["box", "tape", "bubble_wrap"],
                        "weight_limit_kg": 30.0,
                    },
                    "shipping": {
                        "description": "Доставка заказа",
                        "carriers": ["fedex", "ups", "dhl"],
                        "tracking": True,
                        "address_validation": {
                            "strict": True,
                            "fallback": "contact_customer",
                        },
                    },
                    "completion": {
                        "description": "Завершение заказа",
                        "final_actions": [
                            "send_confirmation_email",
                            "update_customer_loyalty_points",
                            "request_feedback",
                        ],
                        "success_metrics": {
                            "avg_process_time_min": 45.2,
                            "success_rate_percent": 98.7,
                        },
                    },
                },
                "metadata": {
                    "author": "business_analytics_team",
                    "last_updated": "2024-05-15",
                    "dependencies": ["inventory_system", "payment_gateway"],
                },
            },
            "Some short bot response"
        )
    
    async def update_schema(self, message: str, schema: dict[str, Any]) -> dict[str, Any]:
        return (
            {
                "process_name": "Обработка заказа в интернет-магазине",
                "version": "1.5",
                "steps": {
                    "payment": {
                        "description": "Оплата заказа",
                        "methods": ["credit_card", "paypal", "bank_transfer"],
                        "retry_count": 3,
                        "on_failure": {
                            "action": "notify_user",
                            "fallback_method": "cash_on_delivery",
                        },
                    },
                    "inventory_check": {
                        "description": "Проверка наличия товаров",
                        "auto": True,
                        "conditions": {
                            "in_stock": {"next_step": "packaging"},
                            "out_of_stock": {
                                "next_step": "notify_supplier",
                                "delay_days": 2,
                            },
                            "partial_stock": {
                                "next_step": "split_shipment",
                                "backorder": True,
                            },
                        },
                    },
                    "packaging": {
                        "description": "Упаковка заказа",
                        "materials": ["box", "tape", "bubble_wrap"],
                        "weight_limit_kg": 30.0,
                    },
                    "shipping": {
                        "description": "Доставка заказа",
                        "carriers": ["fedex", "ups", "dhl"],
                        "tracking": True,
                        "address_validation": {
                            "strict": True,
                            "fallback": "contact_customer",
                        },
                    },
                    "completion": {
                        "description": "Завершение заказа",
                        "final_actions": [
                            "send_confirmation_email",
                            "update_customer_loyalty_points",
                            "request_feedback",
                        ],
                        "success_metrics": {
                            "avg_process_time_min": 45.2,
                            "success_rate_percent": 98.7,
                        },
                    },
                },
                "metadata": {
                    "author": "business_analytics_team",
                    "last_updated": "2024-05-15",
                    "dependencies": ["inventory_system", "payment_gateway"],
                },
            },
            "Bot response on update"
        )
        
    async def generate_chat_name(self, message: str) -> str:
        return "Yet another chat name"
    