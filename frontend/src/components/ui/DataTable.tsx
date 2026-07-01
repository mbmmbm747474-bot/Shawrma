import { type ReactNode } from "react";
import "./DataTable.css";

export interface Column<T> {
  header: string;
  accessor: (row: T) => ReactNode;
  width?: string;
  align?: "start" | "end" | "center";
}

interface DataTableProps<T> {
  columns: Column<T>[];
  rows: T[];
  rowKey: (row: T) => string;
  emptyMessage?: string;
}

export function DataTable<T>({ columns, rows, rowKey, emptyMessage = "لا توجد بيانات" }: DataTableProps<T>) {
  if (rows.length === 0) {
    return <div className="data-table__empty">{emptyMessage}</div>;
  }

  return (
    <div className="data-table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.header} style={{ width: col.width, textAlign: col.align ?? "start" }}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={rowKey(row)}>
              {columns.map((col) => (
                <td key={col.header} style={{ textAlign: col.align ?? "start" }}>
                  {col.accessor(row)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
