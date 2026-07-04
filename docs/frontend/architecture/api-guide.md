# API Guide — Plantão 360

**Sprint:** 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
**Data:** 2026-06-27

---

## Estrutura de Chamadas

### API Client
```typescript
import { apiClient } from 'src/api/client';

// GET
const response = await apiClient.get('/doctors');

// POST
const response = await apiClient.post('/doctors', data);

// PUT
const response = await apiClient.put('/doctors/123', data);

// DELETE
await apiClient.delete('/doctors/123');
```

### Service Layer
```typescript
import { doctorQueries, doctorMutations } from 'src/features/doctor/services/doctor-api';

// Query
const { data, isLoading, error } = useQuery(doctorQueries.list({ name: 'João' }));

// Mutation
const createDoctor = useMutation(doctorMutations.create());
```

### Custom Hooks
```typescript
import { useDoctorList, useCreateDoctor } from 'src/features/doctor/hooks/use-doctors';

// List
const { data, isLoading } = useDoctorList({ name: 'João' });

// Create
const createDoctor = useCreateDoctor();
await createDoctor.mutateAsync({ name: 'Dr. João', crm: '12345' });
```

---

## Error Handling

### Error Types
```typescript
interface AppError {
  message: string;
  code: string;
  status?: number;
  details?: Record<string, string[]>;
}
```

### Error Response
```typescript
const { data, error } = useQuery(doctorQueries.list());

if (error) {
  // error.message is user-friendly
  // error.code is machine-readable
  // error.status is HTTP status
  showSnackbar(error.message, 'error');
}
```

### Error Mapper
```typescript
import { mapErrorToMessage } from 'src/api/client';

const userMessage = mapErrorToMessage(error);
```

---

## Query Keys

### Structure
```typescript
// List
queryKeys.doctors.list({ name: 'João', active: true })

// Detail
queryKeys.doctors.detail('123')

// Invalidation
queryClient.invalidateQueries({ queryKey: queryKeys.doctors.all });
```

### Factory
```typescript
import { queryKeys } from 'src/services/query-keys';

// All keys for a feature
queryKeys.doctors.all // ['doctors']

// List
queryKeys.doctors.list(params) // ['doctors', 'list', params]

// Detail
queryKeys.doctors.detail(id) // ['doctors', 'detail', id]
```

---

## Interceptors

### Request Interceptor
- Adds Authorization header
- Logs request (dev only)

### Response Interceptor
- Maps errors to user-friendly messages
- Logs errors (dev only)
- Retries on network errors (3 attempts)

---

## References

- `frontend/src/api/client.ts`
- `frontend/src/services/query-keys.ts`
- `frontend/src/services/query-factory.ts`
- `docs/api/public-api-contract.md`
