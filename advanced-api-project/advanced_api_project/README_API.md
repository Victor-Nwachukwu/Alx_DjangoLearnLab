# API Views — Book endpoints (advanced-api-project)

This document describes the DRF generic views implemented for the Book model.

## Endpoints

- `GET /api/books/` — BookListView

  - Public: anyone can list books.
  - Supports filtering: `?author=<id>&publication_year=<year>`
  - Supports `?search=<term>` for title search.
  - Ordering via `?ordering=publication_year` or `?ordering=-title`

- `POST /api/books/create/` — BookCreateView

  - Requires authentication.
  - Validates `publication_year` via serializer (cannot be in the future).
  - Returns 201 on success, 400 with validation errors otherwise.

- `GET /api/books/<pk>/` — BookDetailView

  - Public: anyone can retrieve a single Book.

- `PUT/PATCH /api/books/<pk>/update/` — BookUpdateView

  - Requires authentication.
  - Performs serializer validation before saving.

- `DELETE /api/books/<pk>/delete/` — BookDeleteView
  - Restricted to admin users by default (IsAdminUser).
  - To change ownership rules, swap in the custom permission `IsOwnerOrReadOnly`.

## Customization points

- `perform_create()` and `perform_update()` in create/update views: used for setting extra fields (audit fields, created_by, etc.).
- `permission_classes` on each view: change as required (owner-only vs admin-only).
- Filtering and search are wired via `DjangoFilterBackend` + `SearchFilter`.

## Notes

- `BookSerializer` performs publication year validation. Keep domain validation there (not in view).
- If you want to combine list + create into one endpoint, use `generics.ListCreateAPIView` instead of separate `ListAPIView` and `CreateAPIView`.
