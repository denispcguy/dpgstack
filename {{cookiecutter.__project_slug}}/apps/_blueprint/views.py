# Re-export views for backwards compatibility
from .views.table import TableView
from .views.cards import CardView

# Keep original name for compatibility
BlueprintSimpleModelView = TableView

__all__ = ['TableView', 'CardView', 'BlueprintSimpleModelView']