#ifndef __LFS_H__
#define __LFS_H__

#define LFS_DIRECTORY    (0)
#define LFS_REGULAR_FILE (1)

#define LFS_BLOCK_SIZE   (4096)

typedef struct __LFS_Checkpoint_t {
    int loglen;
    int imapents[4096/16]; // entries are -1 if invalid
} LFS_Checkpoint_t;

typedef int LFS_InodeMapEntry_t[16];

typedef struct __LFS_Stat_t {
    int type;   // LFS_DIRECTORY or LFS_REGULAR
    int size;   // bytes
    // note: no permissions, access times, etc.
} LFS_Stat_t;

typedef struct __LFS_DirEnt_t {
    char name[28];  // up to 28 bytes of name in directory (including \0)
    int  inum;      // inode number of entry (-1 means entry not used)
} LFS_DirEnt_t;

typedef struct __LFS_DirBlock_t {
    LFS_DirEnt_t entries[4096/sizeof(LFS_DirEnt_t)];
} LFS_DirBlock_t;

typedef struct __LFS_Inode_t {
    unsigned int len;
    int type; // LFS_DIRECTORY or LFS_REGULAR
    int blockaddr[14]; // The blocks in the file
} LFS_Inode_t;


typedef struct __LFS_Handle_t LFS_Handle_t;

int LFS_Init(LFS_Handle_t *handle, char *filename);
int LFS_Lookup(LFS_Handle_t *handle, int pinum, char *name);
int LFS_Stat(LFS_Handle_t *handle, int inum, int *type, int *size);
int LFS_Write(LFS_Handle_t *handle, int inum, char *buffer, int block);
int LFS_Read(LFS_Handle_t *handle, int inum, char *buffer, int block);
int LFS_Creat(LFS_Handle_t *handle, int pinum, int type, char *name);
int LFS_Unlink(LFS_Handle_t *handle, int pinum, char *name);
int LFS_Close(LFS_Handle_t *handle);

#endif // __LFS_H__
