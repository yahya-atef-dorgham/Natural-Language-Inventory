# Data Model: Natural Language Inventory Dashboard

## Overview

This document describes the key entities involved in the Natural Language Inventory Dashboard and how they relate to each other. It is derived from the feature specification and is implementation-agnostic with respect to specific database schemas.

## Entities

### InventoryItem

- **Description**: Represents a specific product or stock keeping unit (SKU) that can be queried and displayed in the dashboard.  
- **Key Attributes**:  
  - `id`: Unique identifier for the inventory item.  
  - `sku`: External or human-readable SKU code.  
  - `name`: Product name or short description.  
  - `categoryId`: Reference to the item’s product category.  
  - `locationId`: Reference to the primary stocking location (store, warehouse, region).  
  - `currentStock`: Current on-hand stock quantity.  
  - `reorderThreshold`: Quantity below which the item is considered low stock.  
  - `recentSalesVolume`: Aggregated sales over a recent period (for example, last 30 days).  
  - `createdAt` / `updatedAt`: Timestamps for auditing and trend analysis.  
- **Relationships**:  
  - Many `InventoryItem` records belong to one `ProductCategory`.  
  - Many `InventoryItem` records may be associated with one or more locations, depending on how locations are modeled.

### ProductCategory

- **Description**: Logical grouping of inventory items used for filtering and aggregation (for example, “Electronics”, “Home & Garden”).  
- **Key Attributes**:  
  - `id`: Unique identifier for the category.  
  - `name`: Human-readable category name.  
  - `parentCategoryId` (optional): Reference to a parent category for hierarchical structures.  
- **Relationships**:  
  - One `ProductCategory` can have many `InventoryItem` entries.  
  - Categories may form a hierarchy via `parentCategoryId`.

### Location

- **Description**: Represents where inventory is held or sold (for example, stores, warehouses, or regions).  
- **Key Attributes**:  
  - `id`: Unique identifier for the location.  
  - `name`: Human-readable location name.  
  - `type`: Classification (for example, store, warehouse, region).  
  - `parentLocationId` (optional): For hierarchical regions or networks.  
- **Relationships**:  
  - One `Location` can be associated with many inventory items and/or stock records.

### InventoryQuerySession

- **Description**: Captures a single user’s natural language request and the lifecycle of its processing.  
- **Key Attributes**:  
  - `id`: Unique identifier for the session.  
  - `userId`: Reference to the user who initiated the query.  
  - `naturalLanguageQuery`: Original text entered by the user.  
  - `draftQuery`: Initial internal query representation generated from the natural language text.  
  - `reviewFindings`: Structured summary of the self-review step (e.g., flags, adjustments).  
  - `finalQuery`: The refined internal query representation that is actually executed (if approved).  
  - `status`: Lifecycle status (for example, drafted, rejected, executed, failed).  
  - `executedAt`: Timestamp when the final query was executed.  
  - `resultSummary`: High-level summary (for example, number of rows returned, key aggregates).  
- **Relationships**:  
  - One `InventoryQuerySession` belongs to one `User`.  
  - One `InventoryQuerySession` may reference multiple `InventoryItem` or `ProductCategory` records through its results.

### User

- **Description**: Represents a person using the dashboard (for example, analyst, operations manager, warehouse supervisor).  
- **Key Attributes**:  
  - `id`: Unique identifier for the user.  
  - `name`: Display name.  
  - `role`: Role or permission grouping (for example, Analyst, Manager, Admin).  
  - `allowedLocations`: The set of locations or regions whose data the user is permitted to see.  
  - `createdAt` / `updatedAt`: Timestamps for auditing.  
- **Relationships**:  
  - One `User` can create many `InventoryQuerySession` records.  
  - User role and allowed locations constrain visibility into `InventoryItem` and related data.

## Derived Views and Aggregations

The dashboard will rely on derived views or aggregations over base entities to support analytics use cases, such as:

- **LowStockView** (conceptual): Items where `currentStock` <= `reorderThreshold`, optionally filtered by category or location.  
- **TopSellersView** (conceptual): Items ranked by `recentSalesVolume` over a specified time window.  
- **StockOutRiskView** (conceptual): Items whose combination of `currentStock`, `recentSalesVolume`, and replenishment patterns indicate a risk of stock-out within a horizon.

These views are logical constructs used by the NL→query reflection engine rather than mandatory physical tables; they guide the design of internal queries and visualizations.


