type LogoProps = {
  size?: number;
};

export function Logo({ size = 22 }: LogoProps) {
  const inner = Math.round(size / 2.75);
  return (
    <div
      className="rounded-md bg-accent-light dark:bg-accent-dark flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <div
        className="bg-white rounded-sm"
        style={{ width: inner, height: inner }}
      />
    </div>
  );
}