import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { Filter, X, Sliders } from "lucide-react";
import Select from "react-select";

const FiltersContainer = styled.div`
  background: var(--bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
`;

const FiltersHeader = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
`;

const FiltersTitle = styled.h3`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
`;

const ClearButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--danger-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: #dc2626;
  }
`;

const FiltersGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
`;

const FilterGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const FilterLabel = styled.label`
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
`;

const RangeContainer = styled.div`
  display: flex;
  gap: 0.5rem;
  align-items: center;
`;

const RangeInput = styled.input`
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 0.875rem;

  &:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const RangeSeparator = styled.span`
  color: var(--text-secondary);
  font-size: 0.875rem;
`;

const SelectContainer = styled.div`
  .select__control {
    border: 1px solid var(--border-color);
    border-radius: 6px;
    min-height: 38px;
    box-shadow: none;

    &:hover {
      border-color: var(--primary-color);
    }

    &.select__control--is-focused {
      border-color: var(--primary-color);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
  }

  .select__menu {
    border: 1px solid var(--border-color);
    border-radius: 6px;
    box-shadow: var(--shadow-lg);
  }

  .select__option {
    &:hover {
      background: var(--bg-secondary);
    }

    &.select__option--is-selected {
      background: var(--primary-color);
      color: white;
    }
  }
`;

const ActiveFilters = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
`;

const ActiveFilterTag = styled.span`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 500;
`;

const RemoveFilterButton = styled.button`
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;

  &:hover {
    opacity: 0.8;
  }
`;

const Filters = ({ filters, onFilterChange, properties }) => {
  const [localFilters, setLocalFilters] = useState(filters);

  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);

  // Extraire les options uniques pour les filtres
  const cities = [
    ...new Set(properties.map((p) => p.city).filter(Boolean)),
  ].sort();
  const propertyTypes = [
    ...new Set(properties.map((p) => p.type).filter(Boolean)),
  ].sort();
  const bedrooms = [
    ...new Set(properties.map((p) => p.bedrooms).filter(Boolean)),
  ].sort((a, b) => a - b);
  const bathrooms = [
    ...new Set(properties.map((p) => p.bathrooms).filter(Boolean)),
  ].sort((a, b) => a - b);

  const handleFilterChange = (key, value) => {
    const newFilters = { ...localFilters, [key]: value };
    setLocalFilters(newFilters);
    onFilterChange(newFilters);
  };

  const clearAllFilters = () => {
    const defaultFilters = {
      priceRange: [0, 1000000],
      minYield: 0,
      bedrooms: [],
      bathrooms: [],
      maxAge: 100,
      minSurface: 0,
      cities: [],
      propertyTypes: [],
    };
    setLocalFilters(defaultFilters);
    onFilterChange(defaultFilters);
  };

  const removeFilter = (key, value) => {
    if (Array.isArray(localFilters[key])) {
      const newValues = localFilters[key].filter((v) => v !== value);
      handleFilterChange(key, newValues);
    } else if (key === "priceRange") {
      handleFilterChange(key, [0, 1000000]);
    } else if (key === "minYield") {
      handleFilterChange(key, 0);
    } else if (key === "maxAge") {
      handleFilterChange(key, 100);
    } else if (key === "minSurface") {
      handleFilterChange(key, 0);
    }
  };

  const getActiveFiltersCount = () => {
    let count = 0;
    if (localFilters.priceRange[0] > 0 || localFilters.priceRange[1] < 1000000)
      count++;
    if (localFilters.minYield > 0) count++;
    if (localFilters.bedrooms.length > 0) count++;
    if (localFilters.bathrooms.length > 0) count++;
    if (localFilters.maxAge < 100) count++;
    if (localFilters.minSurface > 0) count++;
    if (localFilters.cities.length > 0) count++;
    if (localFilters.propertyTypes.length > 0) count++;
    return count;
  };

  return (
    <FiltersContainer>
      <FiltersHeader>
        <FiltersTitle>
          <Sliders size={20} />
          Filtres ({getActiveFiltersCount()})
        </FiltersTitle>
        <ClearButton onClick={clearAllFilters}>
          <X size={16} />
          Effacer tout
        </ClearButton>
      </FiltersHeader>

      <FiltersGrid>
        <FilterGroup>
          <FilterLabel>Plage de prix</FilterLabel>
          <RangeContainer>
            <RangeInput
              type="number"
              placeholder="Min"
              value={localFilters.priceRange[0]}
              onChange={(e) =>
                handleFilterChange("priceRange", [
                  parseInt(e.target.value) || 0,
                  localFilters.priceRange[1],
                ])
              }
            />
            <RangeSeparator>-</RangeSeparator>
            <RangeInput
              type="number"
              placeholder="Max"
              value={localFilters.priceRange[1]}
              onChange={(e) =>
                handleFilterChange("priceRange", [
                  localFilters.priceRange[0],
                  parseInt(e.target.value) || 1000000,
                ])
              }
            />
          </RangeContainer>
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Rendement minimum (%)</FilterLabel>
          <RangeInput
            type="number"
            placeholder="0"
            value={localFilters.minYield}
            onChange={(e) =>
              handleFilterChange("minYield", parseFloat(e.target.value) || 0)
            }
            step="0.1"
          />
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Nombre de chambres</FilterLabel>
          <SelectContainer>
            <Select
              isMulti
              options={bedrooms.map((b) => ({
                value: b,
                label: `${b} chambre(s)`,
              }))}
              value={localFilters.bedrooms.map((b) => ({
                value: b,
                label: `${b} chambre(s)`,
              }))}
              onChange={(selected) =>
                handleFilterChange(
                  "bedrooms",
                  selected.map((s) => s.value)
                )
              }
              placeholder="Sélectionner..."
              className="select"
            />
          </SelectContainer>
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Nombre de salles de bain</FilterLabel>
          <SelectContainer>
            <Select
              isMulti
              options={bathrooms.map((b) => ({
                value: b,
                label: `${b} salle(s) de bain`,
              }))}
              value={localFilters.bathrooms.map((b) => ({
                value: b,
                label: `${b} salle(s) de bain`,
              }))}
              onChange={(selected) =>
                handleFilterChange(
                  "bathrooms",
                  selected.map((s) => s.value)
                )
              }
              placeholder="Sélectionner..."
              className="select"
            />
          </SelectContainer>
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Âge maximum (années)</FilterLabel>
          <RangeInput
            type="number"
            placeholder="100"
            value={localFilters.maxAge}
            onChange={(e) =>
              handleFilterChange("maxAge", parseInt(e.target.value) || 100)
            }
          />
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Surface minimale (pi²)</FilterLabel>
          <RangeInput
            type="number"
            placeholder="0"
            value={localFilters.minSurface}
            onChange={(e) =>
              handleFilterChange("minSurface", parseInt(e.target.value) || 0)
            }
          />
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Villes</FilterLabel>
          <SelectContainer>
            <Select
              isMulti
              options={cities.map((city) => ({ value: city, label: city }))}
              value={localFilters.cities.map((city) => ({
                value: city,
                label: city,
              }))}
              onChange={(selected) =>
                handleFilterChange(
                  "cities",
                  selected.map((s) => s.value)
                )
              }
              placeholder="Sélectionner..."
              className="select"
            />
          </SelectContainer>
        </FilterGroup>

        <FilterGroup>
          <FilterLabel>Types de propriété</FilterLabel>
          <SelectContainer>
            <Select
              isMulti
              options={propertyTypes.map((type) => ({
                value: type,
                label: type,
              }))}
              value={localFilters.propertyTypes.map((type) => ({
                value: type,
                label: type,
              }))}
              onChange={(selected) =>
                handleFilterChange(
                  "propertyTypes",
                  selected.map((s) => s.value)
                )
              }
              placeholder="Sélectionner..."
              className="select"
            />
          </SelectContainer>
        </FilterGroup>
      </FiltersGrid>

      {getActiveFiltersCount() > 0 && (
        <ActiveFilters>
          {localFilters.priceRange[0] > 0 && (
            <ActiveFilterTag>
              Prix min: ${localFilters.priceRange[0].toLocaleString()}
              <RemoveFilterButton onClick={() => removeFilter("priceRange", 0)}>
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          )}
          {localFilters.priceRange[1] < 1000000 && (
            <ActiveFilterTag>
              Prix max: ${localFilters.priceRange[1].toLocaleString()}
              <RemoveFilterButton onClick={() => removeFilter("priceRange", 1)}>
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          )}
          {localFilters.minYield > 0 && (
            <ActiveFilterTag>
              Rendement min: {localFilters.minYield}%
              <RemoveFilterButton onClick={() => removeFilter("minYield")}>
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          )}
          {localFilters.bedrooms.map((bedroom) => (
            <ActiveFilterTag key={`bedroom-${bedroom}`}>
              {bedroom} chambre(s)
              <RemoveFilterButton
                onClick={() => removeFilter("bedrooms", bedroom)}
              >
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          ))}
          {localFilters.bathrooms.map((bathroom) => (
            <ActiveFilterTag key={`bathroom-${bathroom}`}>
              {bathroom} salle(s) de bain
              <RemoveFilterButton
                onClick={() => removeFilter("bathrooms", bathroom)}
              >
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          ))}
          {localFilters.maxAge < 100 && (
            <ActiveFilterTag>
              Âge max: {localFilters.maxAge} ans
              <RemoveFilterButton onClick={() => removeFilter("maxAge")}>
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          )}
          {localFilters.minSurface > 0 && (
            <ActiveFilterTag>
              Surface min: {localFilters.minSurface} pi²
              <RemoveFilterButton onClick={() => removeFilter("minSurface")}>
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          )}
          {localFilters.cities.map((city) => (
            <ActiveFilterTag key={`city-${city}`}>
              {city}
              <RemoveFilterButton onClick={() => removeFilter("cities", city)}>
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          ))}
          {localFilters.propertyTypes.map((type) => (
            <ActiveFilterTag key={`type-${type}`}>
              {type}
              <RemoveFilterButton
                onClick={() => removeFilter("propertyTypes", type)}
              >
                <X size={12} />
              </RemoveFilterButton>
            </ActiveFilterTag>
          ))}
        </ActiveFilters>
      )}
    </FiltersContainer>
  );
};

export default Filters;
