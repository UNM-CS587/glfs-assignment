/* Skeleton file for implementing the on-disk LFS image */

#include "lfs.h"
#include "lfs_impl.h"

// Initialize and return the LFS handle for state of the open log. Also 
// initialize the log itself if it does now exist.
int LFS_Init(LFS_Handle_t *handle, char *filename)
{
    return -1; // Return 0 for success when implemented
}

int LFS_Lookup(LFS_Handle_t *handle, int pinum, char *name)
{
    return -1; // Return 0 for success when implemented
}

int LFS_Stat(LFS_Handle_t *handle, int inum, int *type, int *size)
{
    return -1; // Return 0 for success when implemented
}

int LFS_Write(LFS_Handle_t *handle, int inum, char *buffer, int block)
{
    return -1; // Return 0 for success when implemented
}

int LFS_Read(LFS_Handle_t *handle, int inum, char *buffer, int block)
{
    return -1; // Return 0 for success when implemented
}

int LFS_Creat(LFS_Handle_t *handle, int pinum, int type, char *name)
{
    return -1; // Return 0 for success when implemented
}

int LFS_Unlink(LFS_Handle_t *handle, int pinum, char *name) 
{
    return -1; // Return 0 for success when implemented
}

int LFS_Close(LFS_Handle_t *handle)
{
    return -1;
}
