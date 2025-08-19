import React, { useState, useMemo } from "react";
import styled from "styled-components";
import {
  useTable,
  useSortBy,
  useFilters,
  usePagination,
  useGlobalFilter,
} from "react-table";
import {
  Table,
  Search,
  Download,
  Eye,
  Star,
  TrendingUp,
  DollarSign,
  MapPin,
  Calendar,
  Home,
} from "lucide-react";

const TableContainer = styled.div`
  background: var(--bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
  overflow: hidden;
`;

const TableHeader = styled.div`
  background: var(--bg-primary);
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
`;

const TableTitle = styled.h3`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
`;

const TableActions = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
`;

const SearchContainer = styled.div`
  position: relative;
  display: flex;
  align-items: center;
`;

const SearchInput = styled.input`
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 0.875rem;
  width: 250px;

  &:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
`;

const SearchIcon = styled.div`
  position: absolute;
  left: 0.75rem;
  color: var(--text-secondary);
`;

const ExportButton = styled.button`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--secondary-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    background: var(--secondary-dark);
  }
`;

const TableWrapper = styled.div`
  overflow-x: auto;
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
`;

const TableHead = styled.thead`
  background: var(--bg-secondary);
`;

const Th = styled.th`
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: var(--text-primary);
  border-bottom: 1px solid var(--border-color);
  cursor: pointer;
  user-select: none;
  white-space: nowrap;

  &:hover {
    background: var(--border-color);
  }

  &.sortable {
    position: relative;

    &::after {
      content: "↕";
      position: absolute;
      right: 0.5rem;
      color: var(--text-secondary);
    }

    &.sort-asc::after {
      content: "↑";
      color: var(--primary-color);
    }

    &.sort-desc::after {
      content: "↓";
      color: var(--primary-color);
    }
  }
`;

const Td = styled.td`
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
`;

const Tr = styled.tr`
  &:hover {
    background: var(--bg-secondary);
  }
`;

const PaginationContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
`;

const PaginationInfo = styled.div`
  font-size: 0.875rem;
  color: var(--text-secondary);
`;

const PaginationControls = styled.div`
  display: flex;
  gap: 0.5rem;
  align-items: center;
`;

const PaginationButton = styled.button`
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;

  &:hover:not(:disabled) {
    background: var(--bg-secondary);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const PageSizeSelect = styled.select`
  padding: 0.5rem;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.875rem;
`;

const ScoreBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  background: ${(props) => {
    if (props.score >= 8) return "var(--success-color)";
    if (props.score >= 6) return "var(--info-color)";
    if (props.score >= 4) return "var(--warning-color)";
    return "var(--danger-color)";
  }};
`;

const YieldBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  background: ${(props) => {
    if (props.yield >= 8) return "var(--success-color)";
    if (props.yield >= 6) return "var(--info-color)";
    if (props.yield >= 4) return "var(--warning-color)";
    return "var(--danger-color)";
  }};
`;

const PropertyTable = ({ properties }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const columns = useMemo(
    () => [
      {
        Header: "Adresse",
        accessor: "address",
        Cell: ({ value }) => (
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <MapPin size={16} />
            {value || "N/A"}
          </div>
        ),
      },
      {
        Header: "Ville",
        accessor: "city",
        Cell: ({ value }) => value || "N/A",
      },
      {
        Header: "Type",
        accessor: "type",
        Cell: ({ value }) => (
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <Home size={16} />
            {value || "N/A"}
          </div>
        ),
      },
      {
        Header: "Prix",
        accessor: "price",
        Cell: ({ value }) => (
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <DollarSign size={16} />
            {value ? `$${value.toLocaleString()}` : "N/A"}
          </div>
        ),
      },
      {
        Header: "Rendement Brut",
        accessor: "grossYield",
        Cell: ({ value }) => (value ? `${value.toFixed(2)}%` : "N/A"),
      },
      {
        Header: "Rendement Net",
        accessor: "netYield",
        Cell: ({ value }) => (
          <YieldBadge yield={value || 0}>
            <TrendingUp size={12} />
            {value ? `${value.toFixed(2)}%` : "N/A"}
          </YieldBadge>
        ),
      },
      {
        Header: "Prix/pi²",
        accessor: "pricePerSqft",
        Cell: ({ value }) => (value ? `$${value.toFixed(0)}` : "N/A"),
      },
      {
        Header: "Cash-Flow Mensuel",
        accessor: "monthlyCashFlow",
        Cell: ({ value }) => (
          <div
            style={{
              color:
                value >= 0 ? "var(--success-color)" : "var(--danger-color)",
              fontWeight: "600",
            }}
          >
            {value ? `$${value.toFixed(0)}` : "N/A"}
          </div>
        ),
      },
      {
        Header: "Âge",
        accessor: "buildingAge",
        Cell: ({ value }) => (
          <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
            <Calendar size={16} />
            {value ? `${value} ans` : "N/A"}
          </div>
        ),
      },
      {
        Header: "Score",
        accessor: "opportunityScore",
        Cell: ({ value }) => (
          <ScoreBadge score={value || 0}>
            <Star size={12} />
            {value ? value.toFixed(1) : "N/A"}
          </ScoreBadge>
        ),
      },
    ],
    []
  );

  const data = useMemo(() => properties, [properties]);

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    page,
    prepareRow,
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,
    state: { pageIndex, pageSize, globalFilter },
    setGlobalFilter,
  } = useTable(
    {
      columns,
      data,
      initialState: { pageIndex: 0, pageSize: 20 },
    },
    useFilters,
    useGlobalFilter,
    useSortBy,
    usePagination
  );

  const exportToCSV = () => {
    const headers = columns.map((col) => col.Header).join(",");
    const csvData = properties
      .map((property) =>
        [
          property.address || "",
          property.city || "",
          property.type || "",
          property.price || "",
          property.grossYield || "",
          property.netYield || "",
          property.pricePerSqft || "",
          property.monthlyCashFlow || "",
          property.buildingAge || "",
          property.opportunityScore || "",
        ].join(",")
      )
      .join("\n");

    const csv = `${headers}\n${csvData}`;
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "proprietes_immobilieres.csv";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <TableContainer>
      <TableHeader>
        <TableTitle>
          <Table size={20} />
          Tableau des Propriétés ({properties.length})
        </TableTitle>
        <TableActions>
          <SearchContainer>
            <SearchIcon>
              <Search size={16} />
            </SearchIcon>
            <SearchInput
              placeholder="Rechercher une propriété..."
              value={globalFilter || ""}
              onChange={(e) => setGlobalFilter(e.target.value)}
            />
          </SearchContainer>
          <ExportButton onClick={exportToCSV}>
            <Download size={16} />
            Exporter CSV
          </ExportButton>
        </TableActions>
      </TableHeader>

      <TableWrapper>
        <StyledTable {...getTableProps()}>
          <TableHead>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <Th
                    {...column.getHeaderProps(column.getSortByToggleProps())}
                    className={`sortable ${
                      column.isSorted
                        ? column.isSortedDesc
                          ? "sort-desc"
                          : "sort-asc"
                        : ""
                    }`}
                  >
                    {column.render("Header")}
                  </Th>
                ))}
              </tr>
            ))}
          </TableHead>
          <tbody {...getTableBodyProps()}>
            {page.map((row) => {
              prepareRow(row);
              return (
                <Tr {...row.getRowProps()}>
                  {row.cells.map((cell) => (
                    <Td {...cell.getCellProps()}>{cell.render("Cell")}</Td>
                  ))}
                </Tr>
              );
            })}
          </tbody>
        </StyledTable>
      </TableWrapper>

      <PaginationContainer>
        <PaginationInfo>
          Affichage de {pageIndex * pageSize + 1} à{" "}
          {Math.min((pageIndex + 1) * pageSize, properties.length)} sur{" "}
          {properties.length} propriétés
        </PaginationInfo>
        <PaginationControls>
          <PaginationButton
            onClick={() => gotoPage(0)}
            disabled={!canPreviousPage}
          >
            {"<<"}
          </PaginationButton>
          <PaginationButton
            onClick={() => previousPage()}
            disabled={!canPreviousPage}
          >
            {"<"}
          </PaginationButton>
          <PaginationButton onClick={() => nextPage()} disabled={!canNextPage}>
            {">"}
          </PaginationButton>
          <PaginationButton
            onClick={() => gotoPage(pageCount - 1)}
            disabled={!canNextPage}
          >
            {">>"}
          </PaginationButton>

          <span
            style={{
              marginLeft: "1rem",
              fontSize: "0.875rem",
              color: "var(--text-secondary)",
            }}
          >
            Page {pageIndex + 1} sur {pageCount}
          </span>

          <PageSizeSelect
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value));
            }}
          >
            {[10, 20, 50, 100].map((pageSize) => (
              <option key={pageSize} value={pageSize}>
                {pageSize} par page
              </option>
            ))}
          </PageSizeSelect>
        </PaginationControls>
      </PaginationContainer>
    </TableContainer>
  );
};

export default PropertyTable;
